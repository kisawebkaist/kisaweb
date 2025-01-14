import pyotp, random

from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
import rest_framework.status as status

from sso.tests import generate_user, get_cookie_value
from .models import *

# Bear with me, things are getting a little racist here.

class SingleCandidateElectionTestCase(APITestCase):
    def setUp(self):
        now = datetime.datetime.now()
        tomorrow = datetime.timedelta(days=1.0) + now
        self.nonkor = 'UKR'
        self.kor = 'KOR'
        self.current_kaist_uid = 0
        self.totp = pyotp.TOTP(pyotp.random_base32())
        self.current_election = Election(start_datetime=now, end_datetime=tomorrow, is_open_public=True, results_out=True)
        self.current_election.full_clean()
        self.current_election.save()
        self.candidate_user = self.generate_another_user(country=self.nonkor, kisa_division=1, totp_secret=self.totp.secret)
        self.candidate_user.save()
        self.candidate = Candidate(account=self.candidate_user, election=self.current_election, is_open_public=True)
        self.candidate.full_clean()
        self.candidate.save()

        self.voter_kor_member = self.generate_another_user(country=self.kor, kisa_division=1, totp_secret=self.totp.secret)
        self.voter_kor_member.save()
        self.voter_kor_nonmem = self.generate_another_user(country=self.kor, kisa_division=0)
        self.voter_kor_nonmem.save()
        self.voter_nonkor_mem = self.generate_another_user(country=self.nonkor, kisa_division=1, totp_secret=self.totp.secret)
        self.voter_nonkor_mem.save()
        self.voter_nonkor_nonmem = self.generate_another_user(country=self.nonkor, kisa_division=0)
        self.voter_nonkor_nonmem.save()

        self.voter_kor_nonmem_vip = self.generate_another_user(country=self.kor, kisa_division=0)
        self.voter_kor_nonmem_vip.save()
        VotingExceptionToken(user=self.voter_kor_nonmem_vip, election=self.current_election).save()

    def generate_another_user(self, *args, **kwargs):
        kwargs['kaist_uid'] = self.current_kaist_uid
        user = generate_user(*args, **kwargs)
        self.current_kaist_uid += 1
        return user[0]

    def test_vote_uneligible(self):
        test_users = [self.voter_kor_nonmem]
        
        for user in test_users:
            client = APIClient()
            client.force_login(user)
            
            r = client.get(reverse('vote'))
            self.assertFalse(r.data['is_eligible'])
            self.assertFalse(r.data['already_voted'])

            r = client.post(
                reverse('vote'),
                {'candidate': self.candidate.slug, 'vote_type': True}
            )
            self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)


    def test_vote_eligible(self):
        test_users = [self.voter_kor_member, self.voter_nonkor_mem, self.voter_nonkor_nonmem, self.voter_kor_nonmem_vip]

        for user in test_users:
            client = APIClient()
            client.force_login(user)

            r = client.get(reverse('vote'))
            self.assertTrue(r.data['is_eligible'])
            self.assertFalse(r.data['already_voted'])

            r = client.post(
                reverse('vote'),
                {'candidate': self.candidate.slug, 'vote_type': True}
            )
            self.assertEqual(r.status_code, status.HTTP_200_OK)

            r = client.get(reverse('vote'))
            self.assertTrue(r.data['is_eligible'])
            self.assertTrue(r.data['already_voted'])

    def test_multiple_vote(self):
        num_votes = [100, 100, 100] #non_kisa, kisa_in_debate, kisa_not_in_debate

        users = []
        current_election = Election.current_or_error()
        for i in range(num_votes[0]):
            users.append(self.generate_another_user(country=self.nonkor, kisa_division=0, totp_secret=self.totp.secret))
        for i in range(num_votes[1]):
            user= self.generate_another_user(kaist_uid=i, country=self.nonkor, kisa_division=0, totp_secret=self.totp.secret)
            DebateAttendance(user=user, election=current_election).save()
            users.append(user)
        for i in range(num_votes[2]):
            users.append(self.generate_another_user(kaist_uid=i, country=self.nonkor, kisa_division=0, totp_secret=self.totp.secret))
        
        decisions = [0]*2

        for user in users:
            client = APIClient()
            client.force_login(user)

            r = client.get(reverse('vote'))
            self.assertTrue(r.data['is_eligible'])
            self.assertFalse(r.data['already_voted'])
            
            choice = random.getrandbits(1)
            decisions[choice] += 1
            if user.is_kisa() and DebateAttendance.objects.filter(user=user, election=current_election).exists():
                decisions[choice] += 1

            r = client.post(
                reverse('vote'),
                {'candidate': self.candidate.slug, 'vote_type': bool(choice)}
            )
            self.assertEqual(r.status_code, status.HTTP_200_OK)

            r = client.get(reverse('vote'))
            self.assertTrue(r.data['is_eligible'])
            self.assertTrue(r.data['already_voted'])

        self.current_election.update_election_result_cache(force=True)
        client = APIClient()
        r = client.get(
            reverse('election-result-detail', kwargs={'slug':self.current_election.slug}),
        )
        self.assertEqual(r.data['result']['yes'], decisions[1])
        self.assertEqual(r.data['result']['no'], decisions[0])

class MultiCandidateElectionTestCase(APITestCase):
    def setUp(self):
        now = datetime.datetime.now()
        tomorrow = datetime.timedelta(days=1.0) + now
        self.nonkor = 'UKR'
        self.kor = 'KOR'
        self.totp = pyotp.TOTP(pyotp.random_base32())
        self.current_election = Election(start_datetime=now, end_datetime=tomorrow, is_open_public=True, results_out=True)
        self.current_election.full_clean()
        self.current_election.save()
        self.current_kaist_uid = 0

        self.candidate_users = list()
        self.candidates = list()
        self.num_candidates = 2

        for i in range(self.num_candidates):
            user = self.generate_another_user(country=self.nonkor, kisa_division=1, totp_secret=self.totp.secret)
            user.save()
            self.candidate_users.append(user)
            candidate = Candidate(account=user, election=self.current_election)
            candidate.full_clean()
            candidate.save()
            self.candidates.append(candidate)

        self.voter_kor_member = self.generate_another_user(country=self.kor, kisa_division=1, totp_secret=self.totp.secret)
        self.voter_kor_member.save()
        self.current_kaist_uid += 1

        self.voter_kor_nonmem = self.generate_another_user(country=self.kor, kisa_division=0)
        self.voter_kor_nonmem.save()
        self.current_kaist_uid += 1

        self.voter_nonkor_mem = self.generate_another_user(country=self.nonkor, kisa_division=1, totp_secret=self.totp.secret)
        self.voter_nonkor_mem.save()
        self.voter_nonkor_nonmem = self.generate_another_user(country=self.nonkor, kisa_division=0)
        self.voter_nonkor_nonmem.save()

        self.voter_kor_nonmem_vip = self.generate_another_user(country=self.kor, kisa_division=0)
        self.voter_kor_nonmem_vip.save()
        VotingExceptionToken(user=self.voter_kor_nonmem_vip, election=self.current_election).save()

    def generate_another_user(self, *args, **kwargs):
        kwargs['kaist_uid'] = self.current_kaist_uid
        user = generate_user(*args, **kwargs)
        self.current_kaist_uid += 1
        return user[0]

    def test_vote_uneligible(self):
        test_users = [self.voter_kor_nonmem]
        
        for user in test_users:
            client = APIClient()
            client.force_login(user)
            
            r = client.get(reverse('vote'))
            self.assertFalse(r.data['is_eligible'])
            self.assertFalse(r.data['already_voted'])

            r = client.post(
                reverse('vote'),
                {'candidate': self.candidates[0].slug, 'vote_type': True}
            )
            self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)


    def test_vote_eligible(self):
        test_users = [self.voter_kor_member, self.voter_nonkor_mem, self.voter_nonkor_nonmem, self.voter_kor_nonmem_vip]

        for user in test_users:
            client = APIClient()
            client.force_login(user)

            r = client.get(reverse('vote'))
            self.assertTrue(r.data['is_eligible'])
            self.assertFalse(r.data['already_voted'])

            r = client.post(
                reverse('vote'),
                {'candidate': self.candidates[random.randrange(0, self.num_candidates)].slug, 'vote_type': True}
            )
            self.assertEqual(r.status_code, status.HTTP_200_OK)

            r = client.get(reverse('vote'))
            self.assertTrue(r.data['is_eligible'])
            self.assertTrue(r.data['already_voted'])


    def test_multiple_vote(self):
        num_votes = [100, 100, 100] #non_kisa, kisa_in_debate, kisa_not_in_debate

        users = []
        current_election = Election.current_or_error()
        for i in range(num_votes[0]):
            users.append(self.generate_another_user(country=self.nonkor, kisa_division=0, totp_secret=self.totp.secret))
        for i in range(num_votes[1]):
            user= self.generate_another_user(kaist_uid=i, country=self.nonkor, kisa_division=0, totp_secret=self.totp.secret)
            DebateAttendance(user=user, election=current_election).save()
            users.append(user)
        for i in range(num_votes[2]):
            users.append(self.generate_another_user(kaist_uid=i, country=self.nonkor, kisa_division=0, totp_secret=self.totp.secret))
        
        candidate_votes = [0]*self.num_candidates

        for user in users:
            client = APIClient()
            client.force_login(user)

            r = client.get(reverse('vote'))
            self.assertTrue(r.data['is_eligible'])
            self.assertFalse(r.data['already_voted'])
            
            candidate_to_vote = random.randrange(0, self.num_candidates)
            candidate_votes[candidate_to_vote] += 1
            if user.is_kisa() and DebateAttendance.objects.filter(user=user, election=current_election).exists():
                candidate_votes[candidate_to_vote] += 1

            r = client.post(
                reverse('vote'),
                {'candidate': self.candidates[candidate_to_vote].slug, 'vote_type': True}
            )
            self.assertEqual(r.status_code, status.HTTP_200_OK)

            r = client.get(reverse('vote'))
            self.assertTrue(r.data['is_eligible'])
            self.assertTrue(r.data['already_voted'])

        self.current_election.update_election_result_cache(force=True)
        client = APIClient()
        r = client.get(
            reverse('election-result-detail', kwargs={'slug':self.current_election.slug}),
        )
        for i in range(self.num_candidates):
            self.assertEqual(r.data['result'][self.candidates[i].slug], candidate_votes[i])
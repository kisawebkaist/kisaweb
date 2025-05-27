import axios from "axios";

export type UserInfo = {
    kaist_uid: number;
    sso_id: string;
    english_name: string;
    full_name: string;
    email: string;
    business_phone: string;
    employeeType: string;
    organization_id: number;
    campus: string;
  }
interface BaseUser {
is_authenticated: boolean,
data: UserInfo | null,
}
export interface AnonymousUser extends BaseUser {
is_authenticated: false,
data: null,
}
export interface AuthenticatedUser extends BaseUser {
    is_authenticated: true,
    data: UserInfo,
}
export type User = AuthenticatedUser | AnonymousUser;
export class AuthAPI {
    static login = () => {
        axios.post(`${process.env.REACT_APP_API_ENDPOINT}/sso/login-init`, {}).then(
            r => {
                if (!r.data['is_authenticated']) {
                    let form = document.createElement('form');
                    form.action = r.data['data']['auth_uri'];
                    form.method = 'POST';
                    for (let key in r.data['data']['payload']) {
                        let input = document.createElement('input');
                        input.type = 'text';
                        input.name = key;
                        input.value = r.data['data']['payload'][key];
                        form.appendChild(input);
                    }
                    document.body.appendChild(form);
                    form.submit();
                }
            }
        );
    }
    static logout = (next: string): Promise<string> => axios.post(`${process.env.REACT_APP_API_ENDPOINT}/sso/logout/`, {next: next}).then(r => r.data['redirect']);
    static getUserInfo = (): Promise<User> => axios.get(`${process.env.REACT_APP_API_ENDPOINT}/sso/userinfo/`).then(r => r.data);
}
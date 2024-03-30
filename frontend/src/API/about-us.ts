import axios from "axios";

export type DivisionT = {
  division_name: string;
  division_description: string;
  head_member_id: number;
  id: number;
};
export type MemberT = {
  id: number;
  name: string;
  image: string; // Link to image basically the src
  year: string;
  semester: string;
  sns_link: string;
  division: number; // Division Primary Key
};
export type InternalBoardMemberT = {
  id: number;
  name: string;
  image: string; // Link to image basically the src
  year: string;
  semester: string;
  sns_link: string;
  position: string;
  division: number;
};

const welfareDivisionDescription = `The Welfare Division is responsible for what its title suggests: <i>the Welfare of the international community at KAIST</i>.\nWe are responsible for reaching out to the international community and take care of any major problems it faces, be the problems related to academics, campus life, or social life in general. Our responsibilities include, but are not limited to:\n- Represent Initiatives and Voice Problems to KAIST Authorities.\n- Conduct programs directly catered to the wellbeing of the international community e.g. <b>KAITalks</b>, <b>TableTalks</b>, etc.\n- Conduct frequent surveys and discussions among the international community regarding their life on campus, in order to ascertain their current problems and interests. This may be done directly or with the tens of country communities we work with.\nWe at KISA Welfare are dedicated to bringing KAIST international students a happier and a more inclusive campus life. Please feel free to use the resources we have compiled for you at the <b>"Welfare"</b> and <b>"Resources"</b> sections of the website. You can play your part in helping us by merely voicing your concerns and/or suggestions through <b>KISA Voice</b> (also in the "Welfare" section)`;
const eventsDivisionDescription = `KISA Events division organizes multiple fun-filled events where KAIST students can throw away their stress. We also aim to increase friendships and interactions among the international community.`;
const pprDivisionDescription = `KISA PPR team believes that promotion is a very important element of KISA's overall marketing program. The promotion team works closely with other divisions to update the international community on KISA's progress.`;
const webDivisionDescription = `Web division manages the KISA website.\nWe have the following goals:\n- Build and design maintainable features that optimize workflows of the whole community as well as the KISA team itself.\n- Work closely with the other divisions in KISA to ensure the website contains relevant and useful information which will help KISA's mission of serving the international community in KAIST.`;
const financeDivisionDescription = `- The KISA Finance and Logistics Division deals with managing all the expenses of KISA, making budgets and proposals for events, and performing all KISA-related transactions.\n- Our division is also tasked to provide logistical needs and man power to other divisions when needed.\n- The current main goal is to get more external companies on board, in order to increase KISA's budget independently by enabling sponshorship.\n- Subsequently, our Division is in charge of the KISA Merch and taking care of the KISA Room's maintenance and accessibility.`;

const divisions: DivisionT[] = [
  {
    id: 1,
    division_name: "Welfare Division",
    division_description: welfareDivisionDescription,
    head_member_id: 10,
  },
  {
    id: 2,
    division_name: "Events Division",
    division_description: eventsDivisionDescription,
    head_member_id: 20,
  },
  {
    id: 3,
    division_name: "Promotions and Public Relations Division",
    division_description: pprDivisionDescription,
    head_member_id: 30,
  },
  {
    id: 4,
    division_name: "Web Division",
    division_description: webDivisionDescription,
    head_member_id: 40,
  },
  {
    id: 5,
    division_name: "Finance Division",
    division_description: financeDivisionDescription,
    head_member_id: 50,
  },
];

const members: MemberT[] = [
  {
    id: 10,
    name: "ASKM Sayeef Uddin",
    image: "https://kisa.kaist.ac.kr/media/BAR017002.jpg",
    year: "2023",
    semester: "Fall",
    sns_link: "https://www.instagram.com/",
    division: 1,
  },
  {
    id: 20,

    name: "Mahnoor Shafiq",
    image: "https://kisa.kaist.ac.kr/media/BAR07843-2.jpg",
    year: "2023",
    semester: "Fall",
    sns_link: "https://www.instagram.com/",
    division: 2,
  },
  {
    id: 30,
    name: "Shubhangi Kumar",
    image: "https://kisa.kaist.ac.kr/media/BAR07849-2.jpg",
    year: "2023",
    semester: "Fall",
    sns_link: "https://www.instagram.com/",
    division: 3,
  },
  {
    id: 40,
    name: "Jonathan Willianto",
    image: "https://kisa.kaist.ac.kr/media/BAR07998-2.jpg",
    year: "2023",
    semester: "Fall",
    sns_link: "https://www.instagram.com/",
    division: 4,
  },
  {
    id: 50,
    name: "Yersultan Doszhan",
    image: "https://kisa.kaist.ac.kr/media/BAR07945-2.jpg",
    year: "2023",
    semester: "Fall",
    sns_link: "https://www.instagram.com/",
    division: 5,
  },
];

const internalBoardMembers: InternalBoardMemberT[] = [
  {
    id: 100,
    name: "Aanya Singh",
    image: "https://kisa.kaist.ac.kr/media/BAR08017-2.jpg",
    year: "2023",
    semester: "Fall",
    sns_link: "https://www.instagram.com/",
    position: "President",
    division: 2,
  },
  {
    id: 200,
    name: "Hein Lin Thant",
    image: "https://kisa.kaist.ac.kr/media/BAR07940-2.jpg",
    year: "2023",
    semester: "Fall",
    sns_link: "https://www.instagram.com/",
    position: "Vice President",
    division: 2,
  },
  {
    id: 300,
    name: "Mahnoor Shafiq",
    image: "https://kisa.kaist.ac.kr/media/BAR07843-2.jpg",
    year: "2023",
    semester: "Fall",
    sns_link: "https://www.instagram.com/",
    position: "Secretary",
    division: 2,
  },
];

export default class AboutUsAPI {
  static members = async (): Promise<MemberT[]> => {
    return axios
      .get(`${process.env.REACT_APP_API_ENDPOINT}about-us/members`)
      .then((resp) => resp.data);
  };
  static internalMembers = (): Promise<InternalBoardMemberT[]> => {
    return axios
      .get(`${process.env.REACT_APP_API_ENDPOINT}about-us/internal-members`)
      .then((resp) => resp.data);
  };
  static divisions = (): Promise<DivisionT[]> => {
    return axios
      .get(`${process.env.REACT_APP_API_ENDPOINT}about-us/divisions`)
      .then((resp) => resp.data);
  };
}

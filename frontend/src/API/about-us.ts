import axios from "axios";
import { RawDraftContentState } from "draft-js";
import { Semester } from "../core/types";

export enum KISADivision {
  WEB = 1,
  FINANCE, 
  PPR,
  EVENTS, 
  WELFARE,
  SECRETARY, 
  VICE_PRESIDENT,
  PRESIDENT,
};

export function getKISADivisionName(division: KISADivision) {
  switch(division) {
    case KISADivision.WEB:
      return "Web";
    case KISADivision.FINANCE:
      return "Finance";
    case KISADivision.PPR:
      return "PPR";
    case KISADivision.EVENTS:
      return "Events";
    case KISADivision.WELFARE:
      return "Welfare";
    case KISADivision.SECRETARY:
      return "Secretary";
    case KISADivision.VICE_PRESIDENT:
      return "Vice President";
    case KISADivision.PRESIDENT:
      return "President";
  }
}

export type KISADivisionContent = {
  division: KISADivision;
  content:  RawDraftContentState;
};

export type KISARole = {
  semester: Semester;
  division: KISADivision;
  is_head: boolean;
};

export type KISAMember = {
  name: string;
  image: string | null; // Link to image basically the src
  sns_link: string | null;
  exp: KISARole[];
};

const welfareDivisionDescription = `The Welfare Division is responsible for what its title suggests: <i>the Welfare of the international community at KAIST</i>.\nWe are responsible for reaching out to the international community and take care of any major problems it faces, be the problems related to academics, campus life, or social life in general. Our responsibilities include, but are not limited to:\n- Represent Initiatives and Voice Problems to KAIST Authorities.\n- Conduct programs directly catered to the wellbeing of the international community e.g. <b>KAITalks</b>, <b>TableTalks</b>, etc.\n- Conduct frequent surveys and discussions among the international community regarding their life on campus, in order to ascertain their current problems and interests. This may be done directly or with the tens of country communities we work with.\nWe at KISA Welfare are dedicated to bringing KAIST international students a happier and a more inclusive campus life. Please feel free to use the resources we have compiled for you at the <b>"Welfare"</b> and <b>"Resources"</b> sections of the website. You can play your part in helping us by merely voicing your concerns and/or suggestions through <b>KISA Voice</b> (also in the "Welfare" section)`;
const eventsDivisionDescription = `KISA Events division organizes multiple fun-filled events where KAIST students can throw away their stress. We also aim to increase friendships and interactions among the international community.`;
const pprDivisionDescription = `KISA PPR team believes that promotion is a very important element of KISA's overall marketing program. The promotion team works closely with other divisions to update the international community on KISA's progress.`;
const webDivisionDescription = `Web division manages the KISA website.\nWe have the following goals:\n- Build and design maintainable features that optimize workflows of the whole community as well as the KISA team itself.\n- Work closely with the other divisions in KISA to ensure the website contains relevant and useful information which will help KISA's mission of serving the international community in KAIST.`;
const financeDivisionDescription = `- The KISA Finance and Logistics Division deals with managing all the expenses of KISA, making budgets and proposals for events, and performing all KISA-related transactions.\n- Our division is also tasked to provide logistical needs and man power to other divisions when needed.\n- The current main goal is to get more external companies on board, in order to increase KISA's budget independently by enabling sponshorship.\n- Subsequently, our Division is in charge of the KISA Merch and taking care of the KISA Room's maintenance and accessibility.`;

export default class AboutUsAPI {
  static getMemberList = async (): Promise<KISAMember[]> => {
    return axios
      .get(`${process.env.REACT_APP_API_ENDPOINT}/about-us/member-list/`)
      .then((resp) => resp.data);
  };
  static getDivisionContentList = async (): Promise<KISADivisionContent[]> => {
    return axios
      .get(`${process.env.REACT_APP_API_ENDPOINT}/about-us/divisions`)
      .then((resp) => resp.data);
  };
}

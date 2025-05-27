import React from "react"
import { NonIndexRouteObject } from "react-router-dom";

type GenericNavEntryT<T, U> = {
  type : T,
  data : U
}

/**
 * @brief describes the structure of data to render a link
 * @param href : url that the link is pointing to
 * @param text : the text to show in the navigation bar
 * @param style : describes the style for the Navigation Bar Link entry
 */
export type NavLinkT = GenericNavEntryT<"link", {
  href : string,
  text : string,
  style? : {
    hover? : React.CSSProperties,
    normal? : React.CSSProperties,
    active? : React.CSSProperties
  }
}>

/**
 * @brief describes the structure of data to render a dropdown.
 */
export type NavDropdownT = GenericNavEntryT<
  "dropdown", {
    display : string
    entries : NavLinkT[]
  }
>

/**
 * @brief the data type for navigation bar entries. A union between NavLinkT and NavDropdownT
 */
type NavEntryT = NavLinkT | NavDropdownT
export default NavEntryT

export type FooterT = {
  location: string;
  phnum_eng: string;
  phnum_kor: string;
  email: string;
  fb_link: string;
  insta_link: string;
  yt_link: string;
}

export interface NavTabRoute extends NonIndexRouteObject {
  path: string;
  tabName: string;
}

export enum Season {
  SPRING = 0,
  SUMMER,
  FALL,
  WINTER,
};

export class Semester {
  season: Season;
  year: number;
  
  static currentSemester = Semester.getCurrentSemester();

  constructor(year: number, season: Season) {
    this.season = season;
    this.year = year;
  }

  static equal(a: Semester, b: Semester) {
    return a.season === b.season && a.year === b.year;
  }

  static getCurrentSeason() {
    let month = new Date(Date.now()).getMonth();
    if (month < 3)
      return Season.WINTER;
    else if (month < 6)
      return Season.SPRING;
    else if (month < 9)
      return Season.SUMMER;
    else if (month < 12)
      return Season.FALL
    return Season.WINTER;
  }

  static getCurrentSemester() {
    let year = new Date(Date.now()).getFullYear();
    let season = Semester.getCurrentSeason()

    return new Semester(year, season);
  }

  static getLastAcademicSemeseter(semesters: Semester[]) {
    return semesters.reduce(
      (acc, curr) => {
        if (acc.year < curr.year)
          return curr;
        if (acc.year > curr.year)
          return acc;
        if (acc.season < curr.season)
          return curr;
        return acc;
      }
    );
  }
};
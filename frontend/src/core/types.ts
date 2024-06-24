import React from "react"

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
  kisa_text: string;
  location: string;
  phnum_eng: string;
  phnum_kor: string;
  email: string;
  fb_link: string;
  insta_link: string;
  yt_link: string;
}

// unstable
export type UserDetail = {
  name: string;
  email: string;
}

export class UserInfo {
  isAuthenticated: boolean;
  detail: UserDetail | null;

  constructor(isAuthenticated: boolean = false, detail: UserDetail | null = null) {
    this.isAuthenticated = isAuthenticated;
    this.detail = detail;
  }
}
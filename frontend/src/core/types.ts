import React from "react"
import { NonIndexRouteObject, RouteObject } from "react-router-dom";

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


export type UserInfo = {
  name: string;
  studentid: string;
  email: string;
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


export interface NavTabRoute extends NonIndexRouteObject {
  path: string;
  tabName: string;
}
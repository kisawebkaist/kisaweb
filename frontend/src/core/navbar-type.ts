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

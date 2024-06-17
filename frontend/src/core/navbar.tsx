import NavEntryT, { NavDropdownT, NavLinkT } from "./types"
import Lister from "../components/lister"
import { Button } from "@mui/material";
import { Link as RouterLink, useLocation } from 'react-router-dom';
import "../components/css/navbar.css"

import fakeNavbarData from "./fakeDataForNavbar";
import React from "react";
import { AuthAPI } from "../API/sso";

type NavbarEntryP = {
  data: NavEntryT
}

export class NavbarP {
  entries: NavEntryT[];
  isAuthenticated: boolean;

  constructor(entries: NavEntryT[] = fakeNavbarData, isAuthenticated:boolean = false) {
    this.entries = entries;
    this.isAuthenticated = isAuthenticated;
  }

  static default(): NavbarP {
    return new NavbarP();
  }
}

const RenderLink = (data: NavLinkT) => {
  const { href, text, style} = data.data
  return (
    <div className="navbar-link">
      <Button component={RouterLink} to={href} color="inherit" className="buttonStyle">
        {text}
      </Button>
    </div>
  );
}

const RenderDropdown = (data: NavDropdownT) => {
  const { display, entries } = data.data
  const [buttonIsHover, setButtonIsHover] = React.useState(false)
  const anchorElement = React.useRef(null)

  function hoverButton() {
    setButtonIsHover(true);
  }

  function leaveButton() {
    setButtonIsHover(false)
  }
  return (
    <div
      className="navbar-dropdown"
      onMouseEnter={hoverButton}
      onMouseLeave={leaveButton}
    >
      <Button
        className="buttonStyle"
        aria-haspopup="true"
        color="inherit"
        aria-controls="dropdown-menu"
        ref={anchorElement}
      >
        {display}
      </Button>
      <div
        className={`navbar-dropdown-menu ${buttonIsHover ? '' : 'hide'}`}
      >
        <Lister
          array={entries}
          render={NavbarEntry}
          props={{}}
        />
      </div>
    </div>
  );
}

export const NavbarEntry = ({ data }: NavbarEntryP) => {
  let renderedElement;

  if (data.type === 'link') {
    renderedElement = RenderLink(data);
  } else if (data.type === 'dropdown') {
    renderedElement = RenderDropdown(data);
  } else {
    renderedElement = <span>Type Error: Please check the type of the navbar entry</span>;
  }

  return (
    <>
      {renderedElement}
    </>
  );
}

const Navbar = ({ entries, isAuthenticated }: NavbarP) => {
  const location = useLocation().pathname;


  return (
    <div className="navbarContainer">
      <RouterLink to = "/">
        <div className="logo">
          <img src="/kisaLogo.png" alt="Kisa Logo" width="75" height="75" />
          <span>KAIST International <br />Student Association</span>
        </div>
      </RouterLink>
      <div className='navbar-links'>
        <Lister
          array={entries}
          render={NavbarEntry}
          props={{}}
        />
      </div>
      <div className = "rightElement">
        <Button 
          className = "rightElement" 
          onClick={isAuthenticated? () => AuthAPI.logout(location).then(redirect => window.location.href = redirect): () => AuthAPI.login(location).then(redirect => window.location.href = redirect)}>
          {isAuthenticated? "LOGOUT": "LOGIN"}
        </Button>
      </div>
    </div >
  )
}

export default Navbar

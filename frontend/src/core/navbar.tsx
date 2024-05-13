import NavEntryT, { NavDropdownT, NavLinkT } from "./navbar-type"
import Lister from "../components/lister"
import { Button } from "@mui/material";
import { Link as RouterLink, useLocation } from 'react-router-dom';
import React, { useEffect } from 'react';
import "../components/css/navbar.css"

type NavbarEntryP = {
  data: NavEntryT
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

type NavbarP = {
  config: NavEntryT[]
}

const Navbar = ({ config }: NavbarP) => {
  
  // testing code, feel free to remove
  // might need to add an extra state for login button to change login, logout
  function getCookies() {
    const cookiesVal = document.cookie.split(";");
    let cookies: {[name: string]: string} = {};
    for (let i=0; i<cookiesVal.length; i++) {
      let pair = cookiesVal[i].split("=");
      cookies[pair[0]] = decodeURIComponent(pair[1]);
    }
    return cookies;
  }
  function login() {
    const endpoint = process.env.REACT_APP_API_ENDPOINT+'/sso/login/';
    fetch(
      endpoint, {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookies()['csrftoken']
        },
        redirect: "manual",
        body: JSON.stringify({"next": useLocation})
      }
    ).then(r => r.json()).then(
      content => {
        window.location.href = content["redirect"];
      });
  }
  function logout() {
    const endpoint = process.env.REACT_APP_API_ENDPOINT+'/sso/logout';
    fetch(
      endpoint, {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookies()['csrftoken']
        },
        redirect: "manual",
        body: JSON.stringify({"next": useLocation})
      }
    ).then(r => r.json()).then(
      content => {
        window.location.href = content["redirect"];
      }
    )
  }

  
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
          array={config}
          render={NavbarEntry}
          props={{}}
        />
      </div>
      <div className = "rightElement">
        <RouterLink to = "/login">
          <Button 
          className = "rightElement" 
          onClick={login}>
            LOGIN
          </Button>
        </RouterLink>
      </div>
    </div >
  )
}

export default Navbar

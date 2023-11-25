import NavEntryT, { NavDropdownT, NavLinkT } from "./navbar-type"
import Lister from "../components/lister"
import { Menu, Button } from "@mui/material";
import { Link as RouterLink } from 'react-router-dom';
import React from 'react';
import "./navbar.css"

type NavbarEntryP = {
  data: NavEntryT
}

const RenderLink = (data: NavLinkT) => {
  const { href, text, style } = data.data
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
  // const [isOpen, setIsOpen] = React.useState(false)
  const [menuIsHover, setMenuIsHover] = React.useState(false)
  const [buttonIsHover, setButtonIsHover] = React.useState(false)
  // const [anchorEl, setAnchorEl] = React.useState<HTMLElement | null>(null);
  const anchorElement = React.useRef(null)
  // function handleOpen() {
  //     setIsOpen(true);
  // }

  // function handleClose() {
  //   setIsOpen(false);
  // }

  function hoverButton() {
    console.log("HoverButton")
    setButtonIsHover(true);
    // if(buttonIsHover || menuIsHover){
    //   setIsOpen(true);
    // }
    // else{
    //   setIsOpen(false);
    // }
  }

  function leaveButton() {
    setButtonIsHover(false)
    console.log("LeaveButton")
    // if(buttonIsHover || menuIsHover){
    //   handleOpen()
    // }
    // else{
    //   handleClose()
    // }
  }

  function hoverMenu() {
    setMenuIsHover(true)
    console.log("HoverMenu")
    // if(buttonIsHover || menuIsHover){
    //   handleOpen()
    // }
    // else{
    //   handleClose()
    // }
  }

  function leaveMenu() {
    setMenuIsHover(false)
    // setButtonIsHover(false)
    console.log("leaveMenu")
    // if(buttonIsHover || menuIsHover){
    //   handleOpen()
    // }
    // else{
    //   handleClose()
    // }
  }
  return (
    <div
      className="navbar-dropdown"
      onMouseEnter={hoverButton}
      //onMouseOver = {handleClick}
      onMouseLeave={leaveButton}
    >
      <Button
      className="buttonStyle"
        aria-haspopup="true"
        color="inherit"
        aria-controls="dropdown-menu"
        ref={anchorElement}
      //onClick={handleClick}
      // onMouseEnter={hoverButton}
      // onMouseOut={leaveButton}
      >
        {display}
      </Button>
      {/* <Menu
        anchorEl={anchorElement.current}
        open={buttonIsHover || menuIsHover}
        // onClose={handleClose}
        MenuListProps={{
          onMouseEnter: hoverMenu,
          onMouseLeave: leaveMenu,
          sx: { py: 0 }
        }}
      > */}
      <div
        className={`navbar-dropdown-menu ${buttonIsHover ? '' : 'hide'}`}
      >
        <Lister
          array={entries}
          render={NavbarEntry}
          props={{}}
        />
      </div>
      {/* </Menu> */}
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
  return (
    <div className="navbarContainer">
      <a href="/home">
        <div className="logo">
          <img src="/kisaLogo.png" alt="Kisa Logo" width="75" height="75" />
          <span>KAIST International <br />Student Association</span>
        </div>
      </a>
      <div className='navbar-links'>
        <Lister
          array={config}
          render={NavbarEntry}
          props={{}}
        />
      </div>
    </div >
  )
}

export default Navbar

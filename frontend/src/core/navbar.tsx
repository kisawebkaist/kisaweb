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
    <div className="buttonStyle">
      <Button component={RouterLink} to={href} color="inherit">
        {text}
      </Button>
    </div>
  );
}

const RenderDropdown = (data: NavDropdownT) => {
  const { display, entries } = data.data
  const [isOpen, setIsOpen] = React.useState(false)
  const [menuIsHover, setMenuIsHover] = React.useState(false)
  const [buttonIsHover, setButtonIsHover] = React.useState(false)
  // const [anchorEl, setAnchorEl] = React.useState<HTMLElement | null>(null);
  const anchorElement = React.useRef(null)
  function handleOpen() {
      setIsOpen(true);
  }

  function handleClose() {
    setIsOpen(false);
  }

  function hoverButton(){
    console.log("HoverButton")
    setButtonIsHover(true);
    if(buttonIsHover || menuIsHover){
      setIsOpen(true);
    }
    else{
      setIsOpen(false);
    }
  }

  function leaveButton(){
    setButtonIsHover(false)
    console.log("LeaveButton")
    if(buttonIsHover || menuIsHover){
      handleOpen()
    }
    else{
      handleClose()
    }
  }

  function hoverMenu(){
    setMenuIsHover(true)
    console.log("HoverMenu")
    if(buttonIsHover || menuIsHover){
      handleOpen()
    }
    else{
      handleClose()
    }
  }

  function leaveMenu(){
    setMenuIsHover(false)
    console.log("leaveMenu")
    if(buttonIsHover || menuIsHover){
      handleOpen()
    }
    else{
      handleClose()
    }
  }
  return (
    <div
      className="buttonStyle"
      onMouseEnter = {hoverButton}
      //onMouseOver = {handleClick}
      onMouseOut = {leaveButton}
    >
      <Button
        aria-haspopup="true"
        color="inherit"
        aria-controls="dropdown-menu"
        ref = {anchorElement}
        //onClick={handleClick}
        onMouseEnter={hoverButton}
        onMouseOut={leaveButton}
      >
        {display}
      </Button>
      <Menu
        anchorEl={anchorElement.current}
        open={isOpen}
        onClose={handleClose}
        MenuListProps={{
          onMouseOver: hoverMenu,
          onMouseOut: leaveMenu,
          sx: { py: 0 }
        }}
      >
        <Lister
          array={entries}
          render={NavbarEntry}
          props={{}}
        />
      </Menu>
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
      <div className="logo">
      <img src="/kisaLogo.png" alt="Kisa Logo" width="75" height="75"/>
      <span>KAIST International <br />Student Association</span>
      </div>
      <Lister
        array={config}
        render={NavbarEntry}
        props={{}}
      />
    </div>
  )
}

export default Navbar

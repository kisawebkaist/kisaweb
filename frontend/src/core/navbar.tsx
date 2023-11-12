import NavEntryT, { NavDropdownT, NavLinkT } from "./navbar-type"
import Lister from "../components/lister"
import { Menu, MenuItem, Button } from "@mui/material";
import { Link as RouterLink } from 'react-router-dom';
import '../components/Css.css'
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
  // const [anchorEl, setAnchorEl] = React.useState<HTMLElement | null>(null);
  const anchorElement = React.useRef(null)
  function handleClick(/*event: React.MouseEvent<HTMLDivElement>*/) {
    // if (anchorEl !== event.currentTarget) {
    //   setAnchorEl(event.currentTarget);
    // }
    setIsOpen(true)
  }

  function handleClose() {
    // setAnchorEl(null);
    setIsOpen(false)
  }
  return (
    <div
      className="buttonStyle"
      onMouseEnter = {handleClick}
    >
      <Button
        aria-haspopup="true"
        color="inherit"
        aria-controls="dropdown-menu"
        ref = {anchorElement}
        // onClick={handleClick}
        // onMouseOver={handleClick}
      >
        {display}
      </Button>
      <Menu
        anchorEl={anchorElement.current}
        open={isOpen}
        // onClose={handleClose}
        MenuListProps={{
          onMouseOut: handleClose,
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

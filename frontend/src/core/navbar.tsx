import NavEntryT, { NavDropdownT, NavLinkT } from "./navbar-type"
import Lister from "../components/lister"
import { Menu, MenuItem, Button } from "@mui/material";
import { Link as RouterLink } from 'react-router-dom';

type NavbarEntryP = {
  data : NavEntryT
}

export const NavbarEntry = ({ data } : NavbarEntryP) => {
    if(data.type === 'link') {
      const { href, text, style } = data.data
    return (
      <Button component={RouterLink} to={href} color="inherit">
      {text}
    </Button>
    );
    }
    else if (data.type === 'dropdown'){
      const { display, entries } = data.data
      return (
        <div>
        <Button aria-haspopup="true" color="inherit" aria-controls="dropdown-menu">
          {display}
        </Button>
        <Menu id="dropdown-menu" anchorOrigin={{ vertical: "bottom", horizontal: "left" }} transformOrigin={{ vertical: "top", horizontal: "left" }}>
          {entries.map((entry, index) => (
            <MenuItem key={index}>
              <NavbarEntry data={entry} />
            </MenuItem>
          ))}
        </Menu>
      </div>
      );
    }
    else{
      //Handle case we want to add more type of navbar entry
      return <span>Type Error: Please check the type of the navbar entry</span>;
    }
}

type NavbarP = {
  config : NavEntryT[]
}

const Navbar = ({ config } : NavbarP) => {
  return (
    <Lister
      array = {config}
      render = {NavbarEntry}
      props = {{}}
    />
  )
}

export default Navbar

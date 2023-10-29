import NavEntryT, { NavDropdownT, NavLinkT } from "./navbar-type"
import Lister from "../components/lister"

type NavbarEntryP = {
  data : NavEntryT
}

export const NavbarEntry = ({ data } : NavbarEntryP) => {
    if(data.type === 'link') {
      const { href, text, style } = data.data
    return (
      <a href={ href }>
        { text }
      </a>
    );
    }
    else if (data.type === 'dropdown'){
      const { display, entries } = data.data
      return (
        <div>
          <p> { display }</p>
          <ul>
          {entries.map((entry, index) => (
            <li key={ index }>
              <NavbarEntry data={ entry } />
            </li>
          ))
          }
          </ul>
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

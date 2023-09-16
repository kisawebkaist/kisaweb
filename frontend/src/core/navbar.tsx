import NavEntryT from "./navbar-type"
import Lister from "../components/lister"

type NavbarEntryP = {
  data : NavEntryT
}

export const NavbarEntry = ({ data } : NavbarEntryP) => {
  return (
    <p>This is a navbar entry</p>
  )
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

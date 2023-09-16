import React from "react"
import { Outlet } from "react-router-dom"
import Footer, { FooterP } from "../../core/footer"
import Navbar from "../../core/navbar"
import NavEntryT from "../../core/navbar-type"

const Main = () => {
  const [navbarConfig, setNavbarConfig] = React.useState<NavEntryT[]>([])
  const [footerConfig, setFooterConfig] = React.useState<FooterP | null>(null)
  // useEffect to query
  return (
    <React.Fragment>
      <header>
        <Navbar config = {navbarConfig} />
      </header>
      <main>
        <Outlet />
      </main>
      {footerConfig && <Footer {...footerConfig} />}
    </React.Fragment>
  )
}

export default Main

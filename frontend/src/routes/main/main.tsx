import React from "react"
import { Outlet } from "react-router-dom"
import Footer, { FooterP } from "../../core/footer"
import Navbar from "../../core/navbar"
import NavEntryT from "../../core/navbar-type"
import "../../components/css/index.css"
import fakeFooterData from "../../core/fakeDataForFooter"
import fakeNavbarData from "../../core/fakeDataForNavbar"

const Main = () => {
  const [navbarConfig, setNavbarConfig] = React.useState<NavEntryT[]>(fakeNavbarData)
  const [footerConfig, setFooterConfig] = React.useState<FooterP>(fakeFooterData)
  // useEffect to query
  return (
    <React.Fragment>
      <header>
        <Navbar config = {navbarConfig} />
      </header>
      <main>
        <div className="mainContent">
          <img src="https://media.tenor.com/CWgfFh7ozHkAAAAC/rick-astly-rick-rolled.gif" width="100%"/>
        </div>
        <Outlet />
      </main>
      {footerConfig && <Footer {...footerConfig} />}
    </React.Fragment>
  )
}

export default Main

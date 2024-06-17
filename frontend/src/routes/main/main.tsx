import React, { useEffect } from "react"
import { Outlet } from "react-router-dom"
import Footer, { FooterP } from "../../core/footer"
import Navbar, { NavbarP } from "../../core/navbar"
import NavEntryT, { FooterT, UserInfo } from "../../core/types"
import "../../components/css/index.css"
import MiscAPI from "../../API/misc"
import { AuthAPI } from "../../API/sso"

const Main = () => {
  const [navbarConfig, setNavbarConfig] = React.useState<NavbarP>(new NavbarP());
  const [footerConfig, setFooterConfig] = React.useState<FooterP>(new FooterP());
  const [userInfo, setUserInfo] = React.useState<UserInfo>(new UserInfo());

  useEffect(
    () => {
      MiscAPI.footer().then((footer:FooterT) => {setFooterConfig(new FooterP(footer))});
      MiscAPI.navbar().then((entries:NavEntryT[]) => {setNavbarConfig(new NavbarP(entries, false))});
      AuthAPI.userinfo().then(setUserInfo);
    }, []
  )

  useEffect(
    () => {
      setNavbarConfig(new NavbarP(navbarConfig.entries, userInfo.is_authenticated));
    }, [navbarConfig.entries, userInfo.is_authenticated]
  )

  return (
    <React.Fragment>
      <header>
        <Navbar entries = {navbarConfig.entries} isAuthenticated = {navbarConfig.isAuthenticated}/>
      </header>
      <main>
        {/* <div className="mainContent">
          <img src="https://media.tenor.com/CWgfFh7ozHkAAAAC/rick-astly-rick-rolled.gif" width="100%"/>
        </div> */}
        <Outlet />
      </main>
      {footerConfig && <Footer {...footerConfig} />}
    </React.Fragment>
  )
}

export default Main

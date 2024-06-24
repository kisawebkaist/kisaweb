import React, { useEffect } from "react"
import { Outlet } from "react-router-dom"
import Footer, { FooterP } from "../../core/footer"
import Navbar, { NavbarP } from "../../core/navbar-alt"
import { FooterT, UserInfo } from "../../core/types"
import "../../components/css/index.css"
import MiscAPI from "../../API/misc"
import { AuthAPI } from "../../API/sso"
import { Divider, Stack } from "@mui/material"

function shouldRenderCompact() {
  const {innerWidth, innerHeight} = window;
  return innerHeight >= innerWidth;
}

const Main = () => {
  const [navbarConfig, setNavbarConfig] = React.useState<NavbarP>(new NavbarP());
  const [footerConfig, setFooterConfig] = React.useState<FooterP>(new FooterP());
  const [userInfo, setUserInfo] = React.useState<UserInfo>(new UserInfo());
  const [compactMode, setCompactMode] = React.useState<boolean>(shouldRenderCompact());

  useEffect(
    () => {
      function handleViewportResize() {
        setCompactMode(shouldRenderCompact);
      }
      MiscAPI.footer().then((footer:FooterT) => {setFooterConfig(new FooterP(footer))});
      // MiscAPI.navbar().then((entries:NavEntryT[]) => {setNavbarConfig(new NavbarP(entries, false))});
      AuthAPI.userinfo().then(setUserInfo);
      window.addEventListener('resize', handleViewportResize)
    }, []
  )

  useEffect(
    () => {
      setNavbarConfig(new NavbarP(navbarConfig.entries, userInfo, navbarConfig.compactMode));
    }, [userInfo]
  )

  useEffect(
    () => {
      setFooterConfig(new FooterP(footerConfig.data, compactMode));
      setNavbarConfig(new NavbarP(navbarConfig.entries, navbarConfig.userInfo, compactMode));
    }, [compactMode]
  )

  return (
    <Stack minHeight="100vh" sx={{ justifyContent: 'space-between' }}>
      <Navbar {...navbarConfig} />
      <main>
        <Outlet />
      </main>
      {footerConfig && <Footer {...footerConfig} />}
    </Stack>
  )
}

export default Main

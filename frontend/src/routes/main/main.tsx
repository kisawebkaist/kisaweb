import React, { useEffect } from "react";
import { Outlet, redirect, useLoaderData, useLocation } from "react-router-dom";
import Footer from "../../core/footer";
import Navbar from "../../core/navbar-alt";
import { FooterT, User } from "../../core/types";

import MiscAPI from "../../API/misc";
import { AuthAPI } from "../../API/sso";
import { tabRoutes } from "./config";
import { Stack } from "@mui/material";

export type MainLoaderData = {
  footerConfig: FooterT;
  compactMode: boolean;
  userInfo: User;
};

export async function mainLoader() {
  return {
    footerConfig: await MiscAPI.footer(),
    userInfo: await AuthAPI.userinfo(),
  };
}

const Main = () => {
  const loaderData = useLoaderData() as MainLoaderData;
  const urlPathSplit = useLocation().pathname.split("/");
  const [currentTab, setCurrentTab] = React.useState<string>(
    urlPathSplit[1] === "" ? tabRoutes[0].path : urlPathSplit[1]
  );

  const mainStyles = React.useMemo(() => {
    return [
      "min-h-[calc(100vh-14rem)]",
      "w-full",
      "p-4",
      "z-10",
      "backdrop-blur"
    ].join(' ')
  }, [])

  const backgroundStyles = React.useMemo(() => {
    return [
      "absolute",
      "z-0",
      "top-20",
      "left-0",
      "min-h-[calc(100vh-14rem)]",
      "w-full",
      "bg-[url('./assets/kisaLogo.png')]",
      "bg-no-repeat",
      "bg-center",
      "bg-fixed",
      "bg-[length:50vh_50vh]",
    ].join(' ')
  }, [])

  return (
    <Stack direction="column">
      <Navbar
        userInfo={loaderData.userInfo}
        currentTab={currentTab}
        setCurrentTab={setCurrentTab}
      />
      <Stack
        className = {backgroundStyles}
      />
      <Stack
        className={mainStyles}
        direction="column"
        component="main"
      >
        <Outlet />
      </Stack>
      <Footer data={loaderData.footerConfig} />
    </Stack>
  );
};

export default Main;

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

export function redirectLoader({ request }: { request: any }) {
  return redirect("/");
}

export async function mainLoader() {
  const compactMode = shouldRenderCompact();
  return {
    footerConfig: await MiscAPI.footer(),
    compactMode: compactMode,
    userInfo: await AuthAPI.userinfo(),
  };
}

function shouldRenderCompact() {
  const { innerWidth, innerHeight } = window;
  return innerHeight >= innerWidth;
}

const Main = () => {
  const loaderData = useLoaderData() as MainLoaderData;
  const urlPathSplit = useLocation().pathname.split("/");
  const [currentTab, setCurrentTab] = React.useState<string>(
    urlPathSplit[1] === "" ? tabRoutes[0].path : urlPathSplit[1]
  );
  const [compactMode, setCompactMode] = React.useState<boolean>(
    shouldRenderCompact()
  );

  useEffect(() => {
    function handleViewportResize() {
      setCompactMode(shouldRenderCompact);
    }
    window.addEventListener("resize", handleViewportResize);
  }, []);

  return (
    <React.Fragment>
      <Navbar
        userInfo={loaderData.userInfo}
        compactMode={compactMode}
        currentTab={currentTab}
        setCurrentTab={setCurrentTab}
      />
      <Stack className = 'min-h-[80vh] w-full' direction = "column" component="main">
        <Outlet />
      </Stack>
      <Footer compactMode={compactMode} data={loaderData.footerConfig} />
    </React.Fragment>
  );
};

export default Main;

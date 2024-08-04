import React, { Reducer, useEffect, useReducer, useState } from "react";
import { Link, Outlet, useLocation } from "react-router-dom";
import Footer from "./footer";
import Navbar from "./navbar-alt";

import { AuthAPI } from "../API/sso";
import { tabRoutes } from "../configs/routes";
import { Drawer, Stack, Tab, Tabs, useColorScheme, useMediaQuery } from "@mui/material";
import AppContext, { AppContextAction, AppContextT, defaultAppContext, DispatcherUpdate, UserUpdate } from "./AppContext";
import { footer } from "../configs/footer";

const Main = () => {
  const urlPathSplit = useLocation().pathname.split("/");
  const [currentTab, setCurrentTab] = React.useState<string>(
    urlPathSplit[1] === "" ? tabRoutes[0].path : urlPathSplit[1]
  );
  const [appContext, dispatch] = useReducer<Reducer<AppContextT, AppContextAction>>((prev, action) => action.dispatch(prev), defaultAppContext);
  const [drawerOpen, setDrawerOpen] = useState<boolean>(false);
  const {setColorScheme} = useColorScheme();
  const prefersDark = useMediaQuery("(prefers-color-scheme: dark)");

  useEffect(() => {
    dispatch(new DispatcherUpdate(dispatch));
    AuthAPI.userinfo().then((user) => dispatch(new UserUpdate(user)));
    setColorScheme(prefersDark? 'dark': 'light');
  }, [prefersDark, setColorScheme])

  const mainStyles = React.useMemo(() => {
    return [
      "min-h-[calc(100vh-14rem)]",
      "w-full",
      "p-4",
      "backdrop-blur",
      "box-border"
    ].join(' ')
  }, [])

  const backgroundStyles = React.useMemo(() => {
    return [
      "absolute",
      "left-0",
      "min-h-screen",
      "w-full",
      "bg-[url('./assets/kisaLogo.png')]",
      "bg-no-repeat",
      "bg-center",
      "bg-fixed",
      "bg-[length:50vh_50vh]",
    ].join(' ')
  }, [])

  return (
    <AppContext.Provider value={appContext} >
      <Stack direction="column" className={backgroundStyles}>
      <Navbar
        currentTab={currentTab}
        setCurrentTab={setCurrentTab}
        drawerOpen={drawerOpen}
        setDrawerOpen={setDrawerOpen}
      />
      <Drawer
        open={drawerOpen}
        PaperProps={{
          sx: { marginTop: "var(--appbar-height)" },
        }}
        sx={{ flexShrink: 0 }}
        onClose={() => setDrawerOpen(false)}
      >
         <Tabs
          variant="scrollable"
          orientation={"vertical"}
          scrollButtons="auto"
          value={currentTab}
          onChange={(_, value) => setCurrentTab(value)}
        >
          {tabRoutes.map((tabRoute) => 
            <Tab
              label={tabRoute.tabName}
              value={tabRoute.path}
              component={Link}
              to={tabRoute.path}
            />
          )}
        </Tabs>
      </Drawer>
      <Stack
        className={mainStyles}
        direction="column"
        component="main"
      >
        <Outlet />
      </Stack>
      <Footer data={footer} />
    </Stack>
    </AppContext.Provider>
  );
};

export default Main;

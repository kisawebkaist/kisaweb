import React, { useEffect, useState } from "react";
import { Link, Outlet, useLocation } from "react-router-dom";
import Footer from "./footer";
import Navbar from "./navbar-alt";

import { AuthAPI, User } from "../API/sso";
import { tabRoutes } from "../configs/routes";
import { Drawer, Snackbar, Stack, Tab, Tabs, useColorScheme, useMediaQuery } from "@mui/material";
import { AuthContext } from "./AuthContext";
import { footer } from "../configs/footer";
import NotificationContext, { Notification } from "./NotificationContext";

const Main = () => {
  const urlPathSplit = useLocation().pathname.split("/");
  const [currentTab, setCurrentTab] = React.useState<string>(
    urlPathSplit[1] === "" ? tabRoutes[0].path : urlPathSplit[1]
  );
  const [drawerOpen, setDrawerOpen] = useState<boolean>(false);

  const { setColorScheme } = useColorScheme();
  const prefersDark = useMediaQuery("(prefers-color-scheme: dark)");

  // contexts
  const [authContextUser, setAuthContextUser] = useState<User>({
    is_authenticated: false,
    data: null
  });
  const authContext = {
    user: authContextUser,
    updateUser: setAuthContextUser
  }

  const [notificationContextData, setNotificationContextData] = useState<Notification>({
    message: "",
    anchorOrigin: {horizontal: "left", vertical: "bottom"},
    open: false,
    autoHideDuration: 3000,
    onClose: (event: React.SyntheticEvent | Event, reason: string) => {}
  })
  const notificationContext = {
    notification: notificationContextData,
    updateNotification: setNotificationContextData,
    showNotification: (message: String) => {
      setNotificationContextData({
        message: message,
        anchorOrigin: {
          vertical: "bottom",
          horizontal: "left"
        },
        open: true,
        autoHideDuration: 3000,
        onClose: (event: React.SyntheticEvent | Event, reason: string) => {
          setNotificationContextData({
            message: "",
            anchorOrigin: {
              vertical: "bottom",
              horizontal: "left",
            },
            open: false,
            autoHideDuration: 3000,
            onClose: (event, reason) => {
              setNotificationContextData({
                message: message,
                anchorOrigin: {
                  vertical: "bottom",
                  horizontal: "left"
                },
                open: false,
                autoHideDuration: 3000,
                onClose: (event, reason) => {}
              })
            }
          })
        }
      })
    }
  };


  useEffect(() => {
    AuthAPI.userinfo().then(setAuthContextUser);
    setColorScheme(prefersDark ? 'dark' : 'light');
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
    <AuthContext.Provider value={authContext} >
      <NotificationContext.Provider value={notificationContext}>
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
            sx: { marginTop: "var(--AppBar-height)" },
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
                key={tabRoute.path}
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
        <Snackbar
                anchorOrigin={notificationContextData.anchorOrigin}
                open={notificationContextData.open}
                message={notificationContextData.message}
                autoHideDuration={notificationContextData.autoHideDuration}
                onClose={notificationContextData.onClose}
            />
      </Stack>
      </NotificationContext.Provider>
    </AuthContext.Provider>
  );
};

export default Main;

import React, { useEffect, useState } from "react";
import { Link, Outlet, useLocation } from "react-router-dom";
import Footer from "./Footer";
import Navbar from "./Navbar";

import { tabRoutes } from "../configs/routes";
import { Drawer, Stack, Tab, Tabs, useColorScheme, useMediaQuery } from "@mui/material";
import { AuthProvider } from "./AuthProvider";
import { footer } from "../configs/footer";
import { NotificationProvider } from "./NotificationProvider";
import DialogProvider from "./PopupProvider";

const Main = () => {
  const urlPathSplit = useLocation().pathname.split("/");
  const [currentTab, setCurrentTab] = React.useState<string>(
    urlPathSplit[1] === "" ? tabRoutes[0].path : urlPathSplit[1]
  );
  const [drawerOpen, setDrawerOpen] = useState<boolean>(false);

  const { setColorScheme } = useColorScheme();
  const prefersDark = useMediaQuery("(prefers-color-scheme: dark)");

  useEffect(() => {
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
    <AuthProvider>
      <NotificationProvider>
        <DialogProvider>
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
        </Stack>
        </DialogProvider>
      </NotificationProvider>
    </AuthProvider>
  );
};

export default Main;

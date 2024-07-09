import { Link } from "react-router-dom";
import {
  AppBar,
  Avatar,
  Box,
  Button,
  Card,
  CardActions,
  CardContent,
  CardHeader,
  Dialog,
  Drawer,
  IconButton,
  Stack,
  Tab,
  Tabs,
  Toolbar,
  Tooltip,
  Typography,
} from "@mui/material";

// import MenuIcon from '@mui/icons-material/Menu';
// import MenuOpenIcon from '@mui/icons-material/MenuOpen';
// import LoginIcon from '@mui/icons-material/Login'
// import LogoutIcon from '@mui/icons-material/Logout'
// import PrivacyTipIcon from '@mui/icons-material/PrivacyTip';

import React, { useState } from "react";
import { AuthAPI } from "../API/sso";
import { tabRoutes } from "../routes/main/config";
import { NavTabRoute, User, UserInfo } from "./types";

import "../components/css/navbar.css";
import { personalInfoUsage } from "./personalInfoUsage";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faBars,
  faRightFromBracket,
  faRightToBracket,
  faShield,
  faXmark,
} from "@fortawesome/free-solid-svg-icons";

export const navbarHeight = "75px";

export type NavbarP = {
  userInfo: User;
  currentTab: string;
  setCurrentTab: React.Dispatch<React.SetStateAction<string>>;
};

const renderNavTab = (data: NavTabRoute) => (
  <Tab
    label={data.tabName}
    value={data.path}
    component={Link}
    to={data.path}
  />
);

const renderAuthMenu = (
  { is_authenticated, data }: User,
) => {
  const SettingsDialog = (user: UserInfo) => {
    const [open, setOpen] = useState<boolean>(false);
    const toggleOpen = () => setOpen(!open);

    const nameAvatar = (name: string) => (
      <Avatar>{name.length === 0 ? "?" : name[0]}</Avatar>
    );
    const accountSettingsContent = [
      <Card>
        <CardHeader
          avatar={nameAvatar(user.name)}
          title={user.name}
          subheader={user.email}
          action={
            <Tooltip title="Personal data usage notice">
              <IconButton onClick={() => setDialogContent(dataCollectionInfo)}>
                <FontAwesomeIcon icon={faShield} />
              </IconButton>
            </Tooltip>
          }
        />
        <CardContent></CardContent>
        <CardActions>
          <Button
            onClick={() =>
              AuthAPI.logout("/").then(
                (redirect) => (window.location.href = redirect)
              )
            }
          >
            <FontAwesomeIcon icon={faRightFromBracket} />
            Logout
          </Button>
        </CardActions>
      </Card>,
    ];
    const dataCollectionInfo = [
      <Card>
        <CardHeader
          title="Personal Information Usage Disclosure"
          subheader={"Last Modified: " + personalInfoUsage.lastModified}
        />
        {personalInfoUsage.statement}
        <CardActions>
          <Button onClick={() => setDialogContent(accountSettingsContent)}>
            Back
          </Button>
          <Button color="secondary">delete my account</Button>
        </CardActions>
      </Card>,
    ];

    const [dialogContent, setDialogContent] = useState<React.ReactElement[]>(
      accountSettingsContent
    );

    return (
      <React.Fragment>
        <Tooltip title="Account Settings">
          <IconButton onClick={toggleOpen}>{nameAvatar(user.name)}</IconButton>
        </Tooltip>
        <Dialog open={open} onClose={() => setOpen(false)}>
          {dialogContent}
        </Dialog>
      </React.Fragment>
    );
  };

  return is_authenticated ? (
    <SettingsDialog {...data} />
  ) : [(
    <Tooltip title="Login" sx={{ display: {xs: 'block', md: 'none'} }}>
      <IconButton
        onClick={() =>
          AuthAPI.login("/").then(
            (redirect) => (window.location.href = redirect)
          )
        }
      >
        <FontAwesomeIcon icon={faRightToBracket} />
      </IconButton>
    </Tooltip>
  ) , (
    <Button
      onClick={() =>
        AuthAPI.login("/").then((redirect) => (window.location.href = redirect))
      }
      sx={{ display: {xs: 'none', md: 'block'} }}
    >
      <FontAwesomeIcon icon={faRightToBracket} />
      LOGIN
    </Button>
  )];
};

const Navbar = ({
  userInfo,
  currentTab,
  setCurrentTab,
}: NavbarP) => {
  const [drawerOpen, setDrawerOpen] = useState<boolean>(false);
  console.log(currentTab);

  const handleDrawerMenuOnClick = (event: React.SyntheticEvent) =>
    setDrawerOpen(!drawerOpen);

  const navMenuButton = (drawerOpen: boolean) => {
    const CustomTooltip = (props: { children: JSX.Element }) =>
      drawerOpen ? (
        <Box sx={{display: {xs: 'block', sm: 'none'}}}>{props.children}</Box>
      ) : (
        <Tooltip title="Navigation Menu" sx={{display: {xs: 'block', sm: 'none'}}}>{props.children}</Tooltip>
      );
    return (
      <CustomTooltip>
        <IconButton onClick={handleDrawerMenuOnClick}>
          {drawerOpen ? (
            <FontAwesomeIcon icon={faXmark} />
          ) : (
            <FontAwesomeIcon icon={faBars} />
          )}
        </IconButton>
      </CustomTooltip>
    );
  };

  return (
    <React.Fragment>
      <AppBar
        className="sticky top-0 left-0 h-20"
        sx={{
          zIndex: (theme) => theme.zIndex.drawer + 1,
        }}
      >
        <Toolbar sx={{ justifyContent: "space-between" }}>
          {navMenuButton(drawerOpen)}
          <Box
            component="img"
            src="/kisaLogo.png"
            alt="KISA Logo"
            sx={{ height: "100%" }}
          />
           <Tabs
            variant="scrollable"
            orientation="horizontal"
            scrollButtons="auto"
            value={currentTab}
            onChange={(_, value) => setCurrentTab(value)}
            sx={{display: {xs: 'none', sm: 'block'}}}
            >
            {tabRoutes.map(renderNavTab)}
          </Tabs>
          {renderAuthMenu(userInfo)}
        </Toolbar>
      </AppBar>
      <Drawer
        open={drawerOpen}
        PaperProps={{
          sx: { marginTop: navbarHeight },
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
          {tabRoutes.map(renderNavTab)}
        </Tabs>
      </Drawer>
    </React.Fragment>
  );
};
export default Navbar;

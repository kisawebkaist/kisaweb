import { Link } from 'react-router-dom';
import { AppBar, Avatar, Box, Button, Card, CardActions, CardContent, CardHeader, Dialog, Drawer, IconButton, Stack, Tab, Tabs, Toolbar, Tooltip, Typography } from "@mui/material";

import MenuIcon from '@mui/icons-material/Menu';
import MenuOpenIcon from '@mui/icons-material/MenuOpen';
import LoginIcon from '@mui/icons-material/Login'
import LogoutIcon from '@mui/icons-material/Logout'
import PrivacyTipIcon from '@mui/icons-material/PrivacyTip';

import React, { useState } from "react";
import { AuthAPI } from "../API/sso";
import { tabRoutes } from "../routes/main/config";
import { NavTabRoute, User, UserInfo } from "./types"

import "../components/css/navbar.css"
import { personalInfoUsage } from './personalInfoUsage';

export const navbarHeight = "75px";

export type NavbarP = {
  userInfo: User;
  compactMode: boolean;
  currentTab: string;
  setCurrentTab: React.Dispatch<React.SetStateAction<string>>;
}

const RenderNavTab = (data: NavTabRoute) => <Tab label={data.tabName} value={data.path} component={Link} to={data.path}/>;

const RenderAuthMenu = ({ is_authenticated, data }: User, compactMode: boolean) => {
    const SettingsDialog = (user: UserInfo) => {
        const [open, setOpen] = useState<boolean>(false);
        const toggleOpen = () => setOpen(!open);
        
        const nameAvatar = (name:string) => <Avatar>{ (name.length === 0)? "?": name[0] }</Avatar>;
        const accountSettingsContent = [(
            <Card>
                <CardHeader
                    avatar={nameAvatar(user.name)}
                    title={user.name}
                    subheader={user.email}
                    action={
                        <Tooltip title="Personal data usage notice">
                            <IconButton onClick={ ()=>setDialogContent(dataCollectionInfo) }>
                                <PrivacyTipIcon/>
                            </IconButton>
                        </Tooltip>
                    }
                />
                <CardContent>
                    
                </CardContent>
                <CardActions>
                    <Button
                        onClick={ ()=>AuthAPI.logout("/").then(redirect => window.location.href = redirect) }
                    >
                        <LogoutIcon />
                        Logout
                    </Button>
                </CardActions>
            </Card>
        )];
        const dataCollectionInfo = [(
            <Card>
                <CardHeader
                    title="Personal Information Usage Disclosure"
                    subheader={"Last Modified: "+personalInfoUsage.lastModified}
                />
                {personalInfoUsage.statement}
                <CardActions>
                    <Button onClick={ ()=>setDialogContent(accountSettingsContent) }>
                        Back
                    </Button>
                    <Button color='secondary'>
                        delete my account
                    </Button>
                </CardActions>
            </Card>
        )];

        const [dialogContent, setDialogContent] = useState<React.ReactElement[]>(accountSettingsContent);
        
        return (
            <React.Fragment>
                <Tooltip title="Account Settings">
                    <IconButton onClick={toggleOpen}>
                        {nameAvatar(user.name)}
                    </IconButton>
                </Tooltip>
                <Dialog
                    open={open}
                    onClose={ () => setOpen(false) }
                >
                {dialogContent}
                </Dialog>
            </React.Fragment>
            );
    };

    return (
        is_authenticated ? <SettingsDialog {...data} />:
            compactMode ?
            <Tooltip title="Login">
                <IconButton onClick={() => AuthAPI.login("/").then(redirect => window.location.href = redirect)}>
                    <LoginIcon color='primary'/>
                </IconButton>
            </Tooltip>:
            <Button onClick={() => AuthAPI.login("/").then(redirect => window.location.href = redirect)}>
                <LoginIcon /> LOGIN
            </Button>
    );
};

const Navbar = ({ userInfo, compactMode, currentTab, setCurrentTab }: NavbarP) => {
  const [drawerOpen, setDrawerOpen] = useState<boolean>(false);
  console.log(currentTab);

  const handleDrawerMenuOnClick = (event: React.SyntheticEvent) => setDrawerOpen(!drawerOpen);

  const navTabs = (orientation: "horizontal"|"vertical") => (
    <Tabs 
        variant="scrollable" 
        orientation={orientation} 
        scrollButtons="auto" 
        value={currentTab}
        onChange={ (event, value)=>setCurrentTab(value) }
    >
        {tabRoutes.map(RenderNavTab)}
    </Tabs>
  );
  
  const navMenuButton = (drawerOpen: boolean) => {
    const CustomTooltip = (props: { children: JSX.Element }) => drawerOpen? <Box>{props.children}</Box>: <Tooltip title="Navigation Menu">{props.children}</Tooltip>
    return (
        <CustomTooltip>
            <IconButton 
                onClick={handleDrawerMenuOnClick}
            >
                {drawerOpen?<MenuOpenIcon/>:<MenuIcon/>}
            </IconButton>
        </CustomTooltip>
    )
  }

  return (
    <Stack>
    <AppBar sx={{ zIndex: (theme) => theme.zIndex.drawer + 1, height: navbarHeight}}>
        <Toolbar sx={{ justifyContent: 'space-between' }}>
            { compactMode ? navMenuButton(drawerOpen): null }
            <Box
                component="img"
                src="/kisaLogo.png"
                alt="KISA Logo"
                sx={{ height: '100%'}}
            />
            {compactMode ? null : navTabs("horizontal")}
            {RenderAuthMenu(userInfo, compactMode)}
        </Toolbar>
    </AppBar>
    {
        compactMode? 
        <Drawer 
            open={drawerOpen} 
            PaperProps={{ sx: {bgColor: 'primary.main', marginTop: navbarHeight} }} 
            sx={{ flexShrink: 0 }}
            onClose={()=>setDrawerOpen(false)}
        >
           {navTabs("vertical")}
        </Drawer> : null
    }
    </Stack>
    );
}
export default Navbar
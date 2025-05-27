import React, { useCallback } from "react";
import { getKISADivisionName, KISAMember, KISARole } from "../../API/about-us";
import {
  Avatar,
  Box,
  Card,
  CardActionArea,
  CardContent,
  CardHeader,
  CardMedia,
  Divider,
  Grid,
  IconButton,
  Stack,
  Typography,
} from "@mui/material";
import { usePopup } from "../../core/PopupProvider";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCircleXmark } from "@fortawesome/free-solid-svg-icons";

interface ChartMemberDetailProps {
  chartMember: KISAMember;
  position: string;
}

interface ChartMemberProps extends ChartMemberDetailProps{};

const engCardinalPluralRules = new Intl.PluralRules("en", {type: "cardinal"});
const additionalS = (size: number) => engCardinalPluralRules.select(size) === "other"? "s":"";


function ChartMemberDetail(props: ChartMemberDetailProps) {
  let divisionMap = Map.groupBy(props.chartMember.exp, (role) => role.division);  
  let popup = usePopup();

  return (
    <Card>
      <CardHeader 
        title={<Typography variant="h3" align="center">{props.position}</Typography>}
        action={
          <IconButton onClick={()=>{popup.setDialogProps({})}}>
            <FontAwesomeIcon icon={faCircleXmark}/>
          </IconButton>
        }  
        />
        <CardContent component={Grid} container>
          {<CardMedia component="img" src={props.chartMember.image || "/kisaLogo.png"} alt={props.chartMember.name + "'s photo"} sx={{width: "min(100%, 20vw)"}}/>}
          <Typography variant="h3" align="center">
            {props.chartMember.name}
            <Divider/>
          </Typography>
          <Typography align="center">
            {divisionMap.entries().map(([div, divExp]) => [getKISADivisionName(div) + ": " + divExp.length + " semester"+ additionalS(divExp.length), <br/>])}
            <Divider/>
            {props.chartMember.sns_link}
          </Typography>
        </CardContent>
    </Card>
  );
  
}

export function ChartMember(props: ChartMemberProps) {
  const popup = usePopup();
  const onClick = () => {
    popup.setDialogProps({
      children: <ChartMemberDetail {...props}/>,
      onClose: (event, reason) => {
        popup.setDialogProps({});
      }
    });
    popup.show();
  };

  return (
      <Card
        variant="outlined"
        sx={{
          border: "none",
        }}
      >
        <CardActionArea
          onClick={onClick}
        >
          <Box
            sx={{
              display: "flex",
              justifyContent: "center",
            }}
          >
            <CardMedia
              image={props.chartMember.image || "/kisaLogo.png"}
              title={props.position}
              sx={{
                width: "16vw",
                aspectRatio: 1/1,
              }}
            />
          </Box>
          <CardContent
            sx={(theme) => ({
              p: "2vw",
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              alignItems: "center",
              backgroundColor: theme.palette.primary.main,
            })}
          >
              <Typography
                textAlign="center"
                variant="h4"
                sx={(theme)=> ({
                  backgroundColor: theme.palette.background.paper,
                  px: "1vw"
                })}
              >
                {props.position}
              </Typography>
          </CardContent>
        </CardActionArea>
      </Card>
  );
}

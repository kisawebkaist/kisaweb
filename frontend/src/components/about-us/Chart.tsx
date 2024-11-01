import React from "react";
import { DivisionT, InternalBoardMemberT, MemberT } from "../../API/about-us";
import { ChartMember } from "./ChartMember";
import { Card, Grid, Typography } from "@mui/material";
import Divisions from "./Divisions";

interface ChartProps {
  divisions: DivisionT[];
  members: MemberT[];
  internalBoardMembers: InternalBoardMemberT[];
}

export function Chart(props: ChartProps) {
  const president = React.useMemo(
    () =>
      props.internalBoardMembers.find(
        (member) => member.position === "President"
      )!,
    [props.internalBoardMembers]
  );
  const vicePresident = React.useMemo(
    () =>
      props.internalBoardMembers.find(
        (member) => member.position === "Deputy Secretary"
      )!,
    [props.internalBoardMembers]
  );
  const secretary = React.useMemo(
    () =>
      props.internalBoardMembers.find(
        (member) => member.position === "Secretary"
      )!,
    [props.internalBoardMembers]
  );

  return (
      <Grid 
        container
        spacing={"2vw"}
        maxWidth="800px"
      >
        <Grid item xs={12}>
          <ChartMember chartMember={president}/>
        </Grid>
        <Grid item xs={6}>
          <ChartMember chartMember={vicePresident} />
        </Grid>
        <Grid item xs={6}>
        <ChartMember chartMember={secretary} />
        </Grid>
        <Grid item xs={12}>
          <Card
            variant="outlined"
            sx={{
              border: "none",
              p: "2vw"
            }}
          >
            <Typography variant="h3" textAlign="center">
              Divisions
            </Typography>
            <Divisions divisions={[
              {
                name: "Welfare",
                head: {
                  name: "Ahmed",
                  image: "",
                },
                members: ["Alex", "Bob", "Cindy", "Daisy"]
              },
              {
                name: "Web",
                head: {
                  name: "John",
                  image: "",
                },
                members: ["Alex", "Bob", "Cindy", "Daisy", "Euler"]
              }
            ]}/>
          </Card>
        </Grid>
      </Grid>
  );
}

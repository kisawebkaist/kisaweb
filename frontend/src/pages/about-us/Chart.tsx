import React, { useMemo } from "react";
import { KISADivision, KISAMember } from "../../API/about-us";
import { ChartMember } from "./ChartMember";
import { Card, Grid, Typography } from "@mui/material";
import ChartDivisions from "./ChartDivisions";
import { Semester } from "../../core/types";

export interface ChartProps {
  members: KISAMember[];
};

export function Chart(props: ChartProps) {
  const members = useMemo(() => {
    const lastAcademicSemester = Semester.getLastAcademicSemeseter(props.members[0].exp.map(role => role.semester));
    return Map.groupBy(props.members, (member) => member.exp.find((role) => Semester.equal(role.semester, lastAcademicSemester))!.division)
  }, [props.members]);

  const president = members.get(KISADivision.PRESIDENT)?.at(0);
  const vicePresident = members.get(KISADivision.VICE_PRESIDENT)?.at(0);
  const secretary = members.get(KISADivision.SECRETARY)?.at(0);
  const divisions = useMemo(() => {
    let result = new Map(members);
    result.delete(KISADivision.PRESIDENT);
    result.delete(KISADivision.VICE_PRESIDENT);
    result.delete(KISADivision.SECRETARY);
    return result;
  }, [members]);

  return (
      <Grid 
        container
        spacing={"2vw"}
        maxWidth="800px"
      >
        {
          president && 
          <Grid size={{xs: 12}}>
            <ChartMember chartMember={president} position="President"/>
          </Grid>
        }

        <Grid size={{xs: 6}}>
          {vicePresident && <ChartMember chartMember={vicePresident} position="V. President"/>}
        </Grid>
        
        <Grid size={{xs: 6}}>
          {secretary && <ChartMember chartMember={secretary} position="Secretary"/>}
        </Grid>
        
        <Grid size={{xs: 12}}>
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
            <ChartDivisions divisions={divisions} />
          </Card>
        </Grid>
      </Grid>
  );
}

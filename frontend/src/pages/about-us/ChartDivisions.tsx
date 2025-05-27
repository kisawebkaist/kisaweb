import { Avatar, Box, Stack, Tab, Tabs, Typography } from "@mui/material";
import { SetStateAction, useCallback, useMemo, useState } from "react";
import Lister from "../../components/common/Lister";
import { ChartMember } from "./ChartMember";
import { getKISADivisionName, KISADivision, KISAMember } from "../../API/about-us";
import { Semester } from "../../core/types";

interface DivisionsProps {
    divisions: Map<KISADivision, KISAMember[]>;
}

const ChartDivisions = (props: DivisionsProps) => {
    const [value, setValue] = useState<String>(getKISADivisionName(KISADivision.WEB));
    const onChange = (_: any, v: String) => setValue(v);

    const DivisionTabContent = useCallback((division: KISADivision) => {
        let name = getKISADivisionName(division);
        if (name !== value)
            return null;

        let members = props.divisions.get(division)!;
        const lastAcademicSemester = Semester.getLastAcademicSemeseter(members[0].exp.map(role => role.semester));
        let head = members.find((member) => member.exp.find((role) => Semester.equal(role.semester, lastAcademicSemester) && role.is_head));
        return (
            <Stack key={name}>
                <Typography component={"div"}>
                    Members
                    <ul>
                        <li><b>{head?.name || ""}</b> - <i>Head</i></li>
                        {members.map((member) => member !== head && <li key={member.name}>{member.name}</li>)}
                    </ul>
                </Typography>
            </Stack>
        );
    }, [props.divisions, value]);

    const DivisionTab = useCallback((division: KISADivision) => {
        let name = getKISADivisionName(division);
        let members = props.divisions.get(division)!;
        const lastAcademicSemester = Semester.getLastAcademicSemeseter(members[0].exp.map(role => role.semester));
        let head = members.find((member) => member.exp.find((role) => Semester.equal(role.semester, lastAcademicSemester) && role.is_head));
        
        return (
            <Tab 
                value={name}
                label={name}
                key={name}
                icon={<Avatar src={head?.image || "https://i.insider.com/602ee9ced3ad27001837f2ac?width=700" } alt={name + " head"}/>}
            />  
        )
    }, [props.divisions]);
    // TODO: figure out why iter works with the second case but not the first one
    return (
        <>
             <Tabs 
                value={value}
                onChange={onChange}
            >
                {Array.from(props.divisions.keys()).map(DivisionTab)}
            </Tabs>
            {props.divisions.keys().map(DivisionTabContent)}
        </>
    );
};

export default ChartDivisions;
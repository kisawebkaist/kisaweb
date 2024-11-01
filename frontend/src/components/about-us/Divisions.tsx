import { Avatar, Box, Stack, Tab, Tabs, Typography } from "@mui/material";
import { SetStateAction, useMemo, useState } from "react";
import Lister from "../common/Lister";
import { ChartMember } from "./ChartMember";

interface Division {
    name: string;
    head: {
        name: string;
        image: string;
    };
    members: string[];
}

interface DivisionsP {
    divisions: Division[];
}

const Divisions = (props: DivisionsP) => {
    const [value, setValue] = useState<String>(props.divisions[0].name);
    const onChange = (_: any, v: String) => setValue(v);

    const DivisionContent = (data: Division) => {
        if (data.name !== value)
            return null;
        return (
            <Stack key={data.name}>
                <Typography component={"div"}>
                    Members
                    <ul>
                        <li><b>{data.head.name}</b> - <i>Head</i></li>
                        {data.members.map((name) => <li key={name}>{name}</li>)}
                    </ul>
                </Typography>
            </Stack>
        );
    };
    
    return (
        <>
             <Tabs 
                value={value}
                onChange={onChange}
            >
                {props.divisions.map(
                    (data: Division) => 
                        <Tab value={data.name} 
                            label={data.name} 
                            key={data.name} 
                            icon={<Avatar src={data.head.image || "https://i.insider.com/602ee9ced3ad27001837f2ac?width=700"} alt={data.name + " head"}/>}
                        />)}
            </Tabs>
            {props.divisions.map(DivisionContent)}
        </>
    );
};

export default Divisions;
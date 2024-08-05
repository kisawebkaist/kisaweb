import { Button, Card, CardActionArea, CardHeader, CardMedia, Dialog, DialogActions, DialogContent, DialogContentText, Divider, Grid, Stack, Typography } from "@mui/material";
import { EventAPI, EventT_Partial } from "../../API/events";
import Lister from "../../components/common/lister";
import { useLocation } from "react-router-dom";
import HighlightedLetter from "../../components/common/HighlightedLetter";
import QueryGuard from "../../components/common/query-guard";
import { useCallback, useEffect, useRef, useState } from "react";
import TextEditor from "@jowillianto/draftjs-wysiwyg/dist";

function getSemesterFromDate(date: Date) {
    let month = date.getMonth();
    let year = date.getFullYear().toString();
    if (month < 3)
        return year + ' Winter';
    if (month < 7)
        return year + ' Spring';
    if (month < 9)
        return year + ' Summer';
    return year + ' Fall';
}

type EventP = {
    events: EventT_Partial[];
}

export const Event = ({ events }: EventP) => {
    const [dialogOpen, setDialogOpen] = useState<boolean>(false);
    const [slug, setSlug] = useState<string>(useLocation().hash as string);
    const dialogInner = useRef(<></>);

    useEffect(() => {
        if (slug !== "") {
            EventAPI.getEvent(slug)
                .then(event => {
                    setDialogOpen(true);
                    dialogInner.current = (
                        <DialogContent>
                            <Stack>
                                <Typography variant="h3" textAlign="center">
                                    {event.title}
                                </Typography>
                                <TextEditor
                                    defaultValue={event.description}
                                    editorBehaviour={{ readOnly: true }}
                                />
                            </Stack>
                        </DialogContent>
                    );
                })
                .catch(_ => setSlug(""))
        }
    }, [slug])

    const EventCard = useCallback(({ data }: { data: EventT_Partial }) => {
        return (
            <Grid item xs={12} md={6} lg={4}>
                <Card>
                    <CardActionArea
                        onClick={() => setSlug(data.slug)}
                    >
                        <CardMedia
                            component="img"
                            alt={"Poster for " + data.title}
                            image={"https://localhost:8001/media/events/img/zoneoutnight_npeZANa.jpg"}
                        />
                        <CardHeader title={data.important_message} />
                    </CardActionArea>
                </Card>
            </Grid>
        )
    }, []);

    const UpcomingEvents = useCallback(({ events }: EventP) => {
        const now = new Date();
        const toRender = events.filter(event => new Date(event.event_start_datetime) >= now);

        return (
            <Grid container spacing={4} className="p-4">
                <Lister array={toRender} render={EventCard} props={undefined} />
            </Grid>
        )
    }, [EventCard]);

    const renderEventCards = useCallback((events: EventT_Partial[]) => {
        let semesterArchives: JSX.Element[] = [];
        let currentSemester = getSemesterFromDate(new Date());
        let currentSemesterArchive: JSX.Element[] = [];

        function archiveCurrentSemester() {
            if (currentSemesterArchive.length !== 0) {
                semesterArchives.push(<Typography variant="h2">{currentSemester}</Typography>)
                semesterArchives.push(
                    <Grid container spacing={4} className="p-4">
                        {currentSemesterArchive}
                    </Grid>
                );
                semesterArchives.push(<Divider />);
            }
        }

        if (events.length > 0) {
            for (let event of events) {
                let semester = getSemesterFromDate(new Date(event.event_start_datetime));
                if (semester !== currentSemester) {
                    archiveCurrentSemester();
                    currentSemester = semester;
                    currentSemesterArchive = [];
                } else {
                    currentSemesterArchive.push(<EventCard data={event} />);
                }
            }
            archiveCurrentSemester();
        }
        return semesterArchives;
    }, [EventCard]);

    return (
        <Stack>
            <Dialog open={dialogOpen} onClose={() => { setDialogOpen(false); setSlug("") }}>
                {dialogInner.current}
                <DialogActions>
                    <Button>
                        Register
                    </Button>
                </DialogActions>
            </Dialog>
            <Stack textAlign="center">
                <Typography variant="fancy_h1" textAlign="center"><HighlightedLetter letter={"Events"} /></Typography>
                <Typography variant="subtitle1">Live while we're young</Typography>
            </Stack>
            <Typography variant="h2">
                Upcoming Events
            </Typography>
            <UpcomingEvents events={events} />
            <Divider />
            <Typography variant="h2" textAlign="center">All events</Typography>
            <Divider />
            {renderEventCards(events)}
        </Stack>
    )
};

const EventWithGuard = () => {
    const query = (args: Record<string, any>) => EventAPI.allEvents(args).then((events) => {
        return {
            events: events
        }
    })
    return (
        <QueryGuard
            query={query}
            args={{}}
            render={Event}
            props={{}}
        />
    )
}

export default EventWithGuard;
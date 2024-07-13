export type MultimediaT = {
    title: string;
    description: string;
    images: MultimediaImageT[];
};

export type MultimediaImageT = {
    alt: string;
    href: string;
    date: string;
};


export const fakeMultimediaData: MultimediaT[] = [
    {
        title: "2023 Spring OT",
        description: "Never gonna give you up",
        images: [
            {
                alt: "Lorem ipsum",
                href: "https://kisa.kaist.ac.kr/media/images/BAR09659_1.jpg",
                date: "Sat, 13 Jul 2024 06:34:08 GMT",
            },
            {
                alt: "Lorem ipsum",
                href: "https://kisa.kaist.ac.kr/media/images/BAR09659_1.jpg",
                date: "Sat, 13 Jul 2024 06:34:08 GMT",
            },
            {
                alt: "Lorem ipsum",
                href: "https://kisa.kaist.ac.kr/media/images/BAR09659_1.jpg",
                date: "Sat, 13 Jul 2024 06:34:08 GMT",
            }
        ]
    },
    {
        title: "2024 Spring OT",
        description: "Never gonna let you down",
        images: [
            {
                alt: "Lorem ipsum",
                href: "https://kisa.kaist.ac.kr/media/images/BAR09569.jpg",
                date: "Sat, 13 Jul 2024 06:34:08 GMT",
            },
            {
                alt: "Lorem ipsum",
                href: "https://kisa.kaist.ac.kr/media/images/BAR09569.jpg",
                date: "Sat, 13 Jul 2024 06:34:08 GMT",
            },
            {
                alt: "Lorem ipsum",
                href: "https://kisa.kaist.ac.kr/media/images/BAR09569.jpg",
                date: "Sat, 13 Jul 2024 06:34:08 GMT",
            }
        ]
    },
    {
        title: "2025 Spring OT",
        description: "Never gonna run around and desert you",
        images: [
            {
                alt: "Lorem ipsum",
                href: "https://kisa.kaist.ac.kr/media/images/BAR09541.jpg",
                date: "Sat, 13 Jul 2024 06:34:08 GMT",
            },
            {
                alt: "Lorem ipsum",
                href: "https://kisa.kaist.ac.kr/media/images/BAR09541.jpg",
                date: "Sat, 13 Jul 2024 06:34:08 GMT",
            },
            {
                alt: "Lorem ipsum",
                href: "https://kisa.kaist.ac.kr/media/images/BAR09541.jpg",
                date: "Sat, 13 Jul 2024 06:34:08 GMT",
            }
        ]
    }
];
import React from 'react';
import heroImage from '../assets/hero.png';
import {
    Image,
    Container,
    Title,
    Button,
    Group,
    Text,
    List,
    ThemeIcon,
    rem,
} from '@mantine/core';
import { IconCheck } from '@tabler/icons-react';

export default function Hero() {
    const innerStyle = {
        display: 'flex',
        justifyContent: 'space-between',
        paddingTop: `calc(${rem(16)} * 4)`,
        paddingBottom: `calc(${rem(16)} * 4)`,
    };

    const contentStyle = {
        maxWidth: rem(480),
        marginRight: `calc(${rem(16)} * 3)`,
    };

    const titleStyle = {
        color: 'light-dark(var(--mantine-color-black), var(--mantine-color-white))',
        fontFamily: 'Greycliff CF, var(--mantine-font-family)',
        fontSize: rem(44),
        lineHeight: 1.2,
        fontWeight: 900,
    };

    const controlStyle = {
        '@media (maxWidth: $mantineBreakpointXs)': {
            flex: 1,
        },
    };

    const imageStyle = {
        width: rem(376),
        height: rem(356),
    };

    return (
        <Container 
        size="md"
        style={{
            margin: '100px 200px',
            height: '80vh', 
            width: '100vw'
        }}>
            <div style={innerStyle}>
                <div style={contentStyle}>
                    <Title style={titleStyle}>
                        A modern <span style={{ color: '#08a4da' }}>React</span> <br /> based inventory app
                    </Title>
                    <Text c="dimmed" mt="md">
                        Streamline your inventory process with our user-friendly React app built using Mantine components.
                    </Text>

                    <List
                        mt={30}
                        spacing="sm"
                        size="sm"
                        icon={
                            <ThemeIcon size={20} radius="xl">
                                <IconCheck style={{ width: rem(12), height: rem(12) }} stroke={1.5} />
                            </ThemeIcon>
                        }
                    >
                        <List.Item>
                            <b>TypeScript based</b> – Lorem ipsum dolor sit amet consectetur adipisicing elit.
                        </List.Item>
                        <List.Item>
                            <b>Free and open source</b> – Lorem ipsum dolor sit amet consectetur adipisicing elit.
                        </List.Item>
                        <List.Item>
                            <b>No annoying focus ring</b> – Lorem ipsum dolor sit amet consectetur adipisicing elit.
                        </List.Item>
                    </List>

                    <Group mt={30}>
                        <Button radius="xl" size="md" style={controlStyle} >
                            Get started
                        </Button>
                        <Button variant="default" radius="xl" size="md" style={controlStyle}>
                            Source code
                        </Button>
                    </Group>
                </div>
                <Image src={heroImage} style={imageStyle} />
            </div>
        </Container>
    );
}

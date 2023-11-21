import React from 'react';
import { Image, Container, Title, Button, Group, Text, List, ThemeIcon, rem } from '@mantine/core';
import { IconCheck } from '@tabler/icons-react';
import image from '../assets/hero.png';
import classes from './HeroBullets.module.css';

export default function Hero() {
    return (
        <Container size="md">
            <div className={classes.inner}>
                <div className={classes.content}>
                    <Title className={classes.title}>
                        A Modern <Text span c="green" inherit>React</Text> Based Inventory App
                    </Title>
                    <Text c="dimmed" mt="md">
                        Build fully functional accessible web applications faster than ever – Mantine includes
                        more than 120 customizable components and hooks to cover you in any situation
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
                            <b>TypeScript based</b> – build type safe applications, all components and hooks
                            export types
                        </List.Item>
                        <List.Item>
                            <b>Mantine UI</b> – set of components and hooks based on React and TypeScript
                            keyboard
                        </List.Item>
                    </List>

                    <Group mt={30}>
                        <Button radius="xl" size="md" className={classes.control}>
                            Get started
                        </Button>
                        <Button variant="default" radius="xl" size="md" className={classes.control}>
                            Source code
                        </Button>
                    </Group>
                </div>
                <Image src={image} className={classes.image} />
            </div>
        </Container>
    );
}
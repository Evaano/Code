import React from 'react';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Center, Tooltip, UnstyledButton, Stack, rem } from '@mantine/core';
import {
    IconHome2,
    IconGauge,
    IconDeviceDesktopAnalytics,
    IconFingerprint,
    IconCalendarStats,
    IconUser,
    IconSettings,
    IconLogout,
    IconSwitchHorizontal,
} from '@tabler/icons-react';
import { MantineLogo } from '@mantine/ds';
import classes from './NavbarMinimal.module.css';

interface NavbarLinkProps {
    icon: typeof IconHome2;
    label: string;
    active?: boolean;
    onClick?(): void;
}

function NavbarLink({ icon: Icon, label, active, onClick }: NavbarLinkProps) {
    return (
        <Tooltip label={label} position="right" transitionProps={{ duration: 0 }}>
            <UnstyledButton onClick={onClick} className={classes.link} data-active={active || undefined}>
                <Icon style={{ width: rem(20), height: rem(20) }} stroke={1.5} />
            </UnstyledButton>
        </Tooltip>
    );
}

const mockdata = [
    { icon: IconHome2, label: 'Home', path: '/' },
    { icon: IconGauge, label: 'Inventory', path: '/inventory' },
    { icon: IconDeviceDesktopAnalytics, label: 'Add New Item', path: '/new-item' },
    { icon: IconCalendarStats, label: 'Update Items', path: '/update-items' },
    { icon: IconUser, label: 'Account', path: '/account' },
    { icon: IconSettings, label: 'Settings', path: '/settings' },
];

export default function NavbarMinimalColored() {
    const [active, setActive] = useState(2);
    const navigate = useNavigate();

    const links = mockdata.map((link, index) => (
        <NavbarLink
            {...link}
            key={link.label}
            active={index === active}
            onClick={() => {
                setActive(index);
                navigate(link.path);
            }}
        />
    ));

    return (
        <nav className={classes.navbar}>
            <Center>
                <MantineLogo type="mark" inverted size={30} />
            </Center>

            <div className={classes.navbarMain}>
                <Stack justify="center" gap={0}>
                    {links}
                </Stack>
            </div>

            <Stack justify="center" gap={0}>
                <NavbarLink icon={IconLogout} label="Logout" />
            </Stack>
        </nav>
    );
}
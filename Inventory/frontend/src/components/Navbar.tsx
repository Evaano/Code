import React from 'react'
import { useState } from 'react';
import { Center, Stack } from '@mantine/core';
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
import NavbarLink from './NavbarLink';

const navbarStyles = {
    width: '80px',
    height: '100vh',
    padding: 'var(--mantine-spacing-md)',
    display: 'flex',
    flexDirection: 'column' as 'column',
    backgroundColor: 'var(--mantine-color-teal-filled)',
};

const navbarMainStyles = {
    flex: '1',
    marginTop: '50px',
};

const mockdata = [
    { icon: IconHome2, label: 'Home' },
    { icon: IconGauge, label: 'Dashboard' },
    { icon: IconDeviceDesktopAnalytics, label: 'Analytics' },
    { icon: IconCalendarStats, label: 'Releases' },
    { icon: IconUser, label: 'Account' },
    { icon: IconFingerprint, label: 'Security' },
    { icon: IconSettings, label: 'Settings' },
];

export default function Navbar() {
    const [active, setActive] = useState(0); // Set the default active index to 0 for the "Home" icon

    const links = mockdata.map((link, index) => (
        <NavbarLink
            {...link}
            key={link.label}
            active={index === active}
            onClick={() => setActive(index)}
        />
    ));

    return (
        <nav style={navbarStyles}>
            <Center>
                <MantineLogo type="mark" inverted size={30} />
            </Center>

            <div style={navbarMainStyles}>
                <Stack justify="center" gap={0}>
                    {links}
                </Stack>
            </div>

            <Stack justify="center" gap={0}>
                <NavbarLink icon={IconSwitchHorizontal} label="Change account" />
                <NavbarLink icon={IconLogout} label="Logout" />
            </Stack>
        </nav>
    );
}
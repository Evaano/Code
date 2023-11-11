import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
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
    backgroundColor: '#67c369',
};

const navbarMainStyles = {
    flex: '1',
    marginTop: '50px',
};

const mockdata = [
    { icon: IconHome2, label: 'Home', path: '/' },
    { icon: IconGauge, label: 'Inventory', path: '/inventory' },
    { icon: IconDeviceDesktopAnalytics, label: 'Add New Item', path: '/new-item' },
    { icon: IconCalendarStats, label: 'Update Items', path: '/update-items' },
    { icon: IconUser, label: 'Account', path: '/account' },
    { icon: IconFingerprint, label: 'Security', path: '/security' },
    { icon: IconSettings, label: 'Settings', path: '/settings' },
];

const Navbar = () => {
    const navigate = useNavigate();
    const [active, setActive] = useState(0);

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
};

export default Navbar;

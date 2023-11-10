import React from 'react'
import { useState } from 'react';
import { Tooltip, UnstyledButton, rem } from '@mantine/core';
import { IconHome2 } from '@tabler/icons-react';

interface NavbarLinkProps {
    icon: typeof IconHome2;
    label: string;
    active?: boolean;
    onClick?(): void;
}

const linkStyles = {
    width: '50px',
    height: '50px',
    borderRadius: 'var(--mantine-radius-md)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    color: 'var(--mantine-color-white)',
};

const linkHoverStyles = {
    backgroundColor: 'var(--mantine-color-teal-7)',
};

const activeLinkStyles = {
    width: '50px',
    height: '50px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'var(--mantine-color-white)',
    color: 'var(--mantine-color-teal-6)',
    outline: 'none',
};

export default function NavbarLink({ icon: Icon, label, active, onClick }: NavbarLinkProps) {
    const [hovered, setHovered] = useState(false);

    return (
        <Tooltip label={label} position="right" transitionProps={{ duration: 0 }}>
            <UnstyledButton
                onClick={onClick}
                style={{
                    ...linkStyles,
                    ...(active ? activeLinkStyles : {}),
                    ...(hovered && !active ? linkHoverStyles : {}),
                }}
                onMouseOver={() => setHovered(true)}
                onMouseLeave={() => setHovered(false)}
            >
                <Icon style={{ width: rem(20), height: rem(20) }} stroke={1.5} />
            </UnstyledButton>
        </Tooltip>
    );
}
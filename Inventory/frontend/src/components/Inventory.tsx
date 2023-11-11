import React, { useState, useEffect } from 'react';
import { Table, ScrollArea, Input, Select } from '@mantine/core';
import axios from 'axios';

interface InventoryItem {
    item_code: string;
    item_description: string;
    category: string;
    subcategory: string;
    unit: string;
    brand: string;
    inwards: number;
    outwards: number;
    current_stock: number;
    reorder: number;
}

export default function Inventory() {
    const [data, setData] = useState<InventoryItem[]>([]);
    const [scrolled, setScrolled] = useState(false);
    const [filter, setFilter] = useState<string>('');
    const [sort, setSort] = useState<string>('');

    useEffect(() => {
        axios.get('http://127.0.0.1:5000/api/inventory')
            .then(response => {
                setData(response.data.inventory);
            })
            .catch(error => {
                console.error('Error fetching data: ', error);
            });
    }, []);

    const filteredData = data.filter(item =>
        item.item_description.toLowerCase().includes(filter.toLowerCase())
    );

    const headerStyle: React.CSSProperties = {
        position: 'sticky',
        top: 0,
        backgroundColor: scrolled ? 'var(--mantine-color-body)' : 'transparent',
        boxShadow: scrolled ? 'var(--mantine-shadow-sm)' : 'none',
        transition: 'box-shadow 150ms ease',
    };

    const rowStyle: React.CSSProperties = {
        height: '50px', // adjust as needed
    };

    const cellStyle: React.CSSProperties = {
        width: '150px', // adjust as needed
        overflow: 'hidden',
        textOverflow: 'ellipsis',
        whiteSpace: 'nowrap',
    };

    const rows = filteredData.map((item: InventoryItem) => (
        <Table.Tr key={item.item_code} style={rowStyle}>
        <Table.Td style={cellStyle}>{item.item_code}</Table.Td>
        <Table.Td style={cellStyle}>{item.item_description}</Table.Td>
        <Table.Td style={cellStyle}>{item.category}</Table.Td>
        <Table.Td style={cellStyle}>{item.subcategory}</Table.Td>
        <Table.Td style={cellStyle}>{item.unit}</Table.Td>
        <Table.Td style={cellStyle}>{item.brand}</Table.Td>
        <Table.Td style={cellStyle}>{item.inwards}</Table.Td>
        <Table.Td style={cellStyle}>{item.outwards}</Table.Td>
        <Table.Td style={cellStyle}>{item.current_stock}</Table.Td>
        <Table.Td style={cellStyle}>{item.reorder}</Table.Td>
    </Table.Tr>
    ));

    return (
        <div style={{ display: 'flex', flexDirection: 'column', height: '90vh', width: '90vw', marginTop: '32px' }}>
            <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '16px', width: '100%' }}>
                <Input
                    placeholder="Search by description"
                    value={filter}
                    onChange={(event) => setFilter(event.currentTarget.value)}
                />
            </div>
            <ScrollArea
                h="90vh"
                w="93vw"
                onScrollPositionChange={({ y }) => setScrolled(y !== 0)}
            >
                <Table miw={1000}>
                    <Table.Thead style={headerStyle}>
                        <Table.Tr>
                            <Table.Th>Item Code</Table.Th>
                            <Table.Th>Item Description</Table.Th>
                            <Table.Th>Category</Table.Th>
                            <Table.Th>Subcategory</Table.Th>
                            <Table.Th>Unit</Table.Th>
                            <Table.Th>Brand</Table.Th>
                            <Table.Th>Inwards</Table.Th>
                            <Table.Th>Outwards</Table.Th>
                            <Table.Th>Current Stock</Table.Th>
                            <Table.Th>Reorder</Table.Th>
                        </Table.Tr>
                    </Table.Thead>
                    <Table.Tbody>{rows}</Table.Tbody>
                </Table>
            </ScrollArea>
        </div>
    );
}

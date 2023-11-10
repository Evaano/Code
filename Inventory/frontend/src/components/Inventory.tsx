import React, { useState, useEffect } from 'react';
import { Table, ScrollArea } from '@mantine/core';
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

    useEffect(() => {
        axios.get('http://127.0.0.1:5000/api/inventory')
            .then(response => {
                setData(response.data.inventory);
            })
            .catch(error => {
                console.error('Error fetching data: ', error);
            });
    }, []);

    const headerStyle: React.CSSProperties = {
        position: 'sticky',
        top: 0,
        backgroundColor: scrolled ? 'var(--mantine-color-body)' : 'transparent',
        boxShadow: scrolled ? 'var(--mantine-shadow-sm)' : 'none',
        transition: 'box-shadow 150ms ease',
    };

    const rows = data.map((item: InventoryItem) => (
        <Table.Tr key={item.item_code}>
            <Table.Td>{item.item_code}</Table.Td>
            <Table.Td>{item.item_description}</Table.Td>
            <Table.Td>{item.category}</Table.Td>
            <Table.Td>{item.subcategory}</Table.Td>
            <Table.Td>{item.unit}</Table.Td>
            <Table.Td>{item.brand}</Table.Td>
            <Table.Td>{item.inwards}</Table.Td>
            <Table.Td>{item.outwards}</Table.Td>
            <Table.Td>{item.current_stock}</Table.Td>
            <Table.Td>{item.reorder}</Table.Td>
        </Table.Tr>
    ));

    return (
        <ScrollArea h={400} onScrollPositionChange={({ y }) => setScrolled(y !== 0)}>
            <Table miw={1200}>
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
    );
}

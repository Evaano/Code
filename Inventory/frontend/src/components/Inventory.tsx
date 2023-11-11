import React, { useState, useEffect } from 'react';
import { Table, ScrollArea, Select } from '@mantine/core';
import axios from 'axios';
import { FaFilter } from 'react-icons/fa';

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
    const [categoryFilter, setCategoryFilter] = useState<string | null>(null);
    const [isFilterExpanded, setIsFilterExpanded] = useState(false);

    useEffect(() => {
        let url = 'http://127.0.0.1:5000/api/inventory';
        if (categoryFilter) {
            url += '?category=' + encodeURIComponent(categoryFilter);
        }

        axios.get(url)
            .then(response => {
                setData(response.data.inventory);
            })
            .catch(error => {
                console.error('Error fetching data: ', error);
            });
    }, [categoryFilter]);


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
        <div>
            <button 
            style={{ backgroundColor: 'white', outline: 'none'}} 
            onClick={() => setIsFilterExpanded(!isFilterExpanded)}>
                <FaFilter style={{ color: 'gray', fontSize: '10px' }}/>
            </button>

            {isFilterExpanded && (
                <Select
                    data={[
                        { value: '', label: 'All' },
                        { value: 'General Items', label: 'General Items' },
                        { value: 'Medical Items', label: 'Medical Items' },
                        { value: 'Narcotic', label: 'Narcotics' },
                    ]}
                    size='sm'
                    value={categoryFilter || ''}
                    placeholder='Filter by category'
                    onChange={value => setCategoryFilter(value)}
                    style={{ width: '200px', marginLeft: '10px', display: 'inline-block' }}
                />
            )}

            <ScrollArea w={1430} h={750}>
                <Table>
                    <Table.Thead>
                        <Table.Tr>
                            <Table.Th style={{ position: 'sticky', top: 0, backgroundColor: '#fff', overflow: 'hidden' }}>Item Code</Table.Th>
                            <Table.Th style={{ position: 'sticky', top: 0, backgroundColor: '#fff', overflow: 'hidden' }}>Item Description</Table.Th>
                            <Table.Th style={{ position: 'sticky', top: 0, backgroundColor: '#fff' }}>Category</Table.Th>
                            <Table.Th style={{ position: 'sticky', top: 0, backgroundColor: '#fff' }}>Subcategory</Table.Th>
                            <Table.Th style={{ position: 'sticky', top: 0, backgroundColor: '#fff' }}>Unit</Table.Th>
                            <Table.Th style={{ position: 'sticky', top: 0, backgroundColor: '#fff' }}>Brand</Table.Th>
                            <Table.Th style={{ position: 'sticky', top: 0, backgroundColor: '#fff' }}>Inwards</Table.Th>
                            <Table.Th style={{ position: 'sticky', top: 0, backgroundColor: '#fff' }}>Outwards</Table.Th>
                            <Table.Th style={{ position: 'sticky', top: 0, backgroundColor: '#fff' }}>Current Stock</Table.Th>
                            <Table.Th style={{ position: 'sticky', top: 0, backgroundColor: '#fff' }}>Reorder</Table.Th>
                        </Table.Tr>
                    </Table.Thead>
                    <Table.Tbody>{rows}</Table.Tbody>
                </Table>
            </ScrollArea>
        </div>
    );
}
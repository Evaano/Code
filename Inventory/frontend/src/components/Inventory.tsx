import React, { useState, useEffect } from 'react';
import { Table, ScrollArea, Select, Pagination, Input } from '@mantine/core';
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
    const [subcategoryFilter, setSubcategoryFilter] = useState<string | null>(null);
    const [isFilterExpanded, setIsFilterExpanded] = useState(false);
    const [currentPage, setCurrentPage] = useState<number>(1);
    const [searchTerm, setSearchTerm] = useState<string>('');
    const itemsPerPage = 14;

    useEffect(() => {
        let url = 'http://127.0.0.1:5000/api/inventory';
        const queryParams: string[] = [];

        if (categoryFilter) {
            queryParams.push(`category=${encodeURIComponent(categoryFilter)}`);
        }

        if (subcategoryFilter) {
            queryParams.push(`subcategory=${encodeURIComponent(subcategoryFilter)}`);
        }

        if (queryParams.length > 0) {
            url += '?' + queryParams.join('&');
        }

        console.log('API URL:', url);
        console.log('Selected Subcategory Filter:', subcategoryFilter);

        axios.get(url)
            .then(response => {
                console.log('API Response:', response.data);
                setData(response.data.inventory);
            })
            .catch(error => {
                console.error('Error fetching data: ', error);
            });
    }, [categoryFilter, subcategoryFilter, currentPage]);

    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;

    const paginatedData = data.slice(startIndex, endIndex);

    const filteredData = data.filter((item) => {
        const searchTermLower = searchTerm.toLowerCase();
        return (
            item.item_description.toLowerCase().includes(searchTermLower)
        );
    });
    
    const paginatedFilteredData = filteredData.slice(startIndex, endIndex);

    const rows = paginatedFilteredData.map((item: InventoryItem) => (
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


    const pageCount = Math.ceil(data.length / itemsPerPage);

    const handlePageChange = (page: number) => {
        setCurrentPage(page);
    }

    const handleSearchChange = (event) => {
        setSearchTerm(event.target.value);
    };


    const subcategoryOptions = categoryFilter === 'General Items' ? [
        { value: '', label: 'All' },
        { value: 'General Items', label: 'General Items' },
        { value: 'Printed Items', label: 'Printed Items' },
        { value: 'Stationary', label: 'Stationary' },
        { value: 'Toners, Cartridges & Drums', label: 'Toners, Cartridges & Drums' }
    ] : categoryFilter === 'Medical Items' ? [
        { value: '', label: 'All' },
        { value: 'Laboratory Consumables', label: 'Laboratory Consumables' },
        { value: 'Laboratory Instruments', label: 'Laboratory Instruments' },
        { value: 'Laboratory Test Kits', label: 'Laboratory Test Kits' },
        { value: 'Medical Consumable', label: 'Medical Consumable' },
        { value: 'Medical Intruments', label: 'Medical Intruments' },
        { value: 'Oncology Items', label: 'Oncology Items' },
        { value: 'Pharmaceuticals', label: 'Pharmaceuticals' },
        { value: 'Radiology Items', label: 'Radiology Items' }
    ] : categoryFilter === 'Narcotic' ? [
        { value: '', label: 'All' },
        { value: 'Narcotic', label: 'Controlled Drugs' }
    ] : [];

    return (
        <div style={{ height: '90vh', marginLeft: '20px' }}>
            <div style={{ display: 'flex', alignItems: 'center', margin: '10px' }}>
                <button
                    style={{ border: 'none', backgroundColor: 'transparent' }}
                    onClick={() => setIsFilterExpanded(!isFilterExpanded)}>
                    <FaFilter style={{ color: 'gray', fontSize: '10px' }} />
                </button>

                {isFilterExpanded && (
                    <>
                        <Select
                            data={[
                                { value: '', label: 'All' },
                                { value: 'General Items', label: 'General Items' },
                                { value: 'Medical Items', label: 'Medical Items' },
                                { value: 'Narcotic', label: 'Narcotic' },
                            ]}
                            size='sm'
                            value={categoryFilter || ''}
                            placeholder='Filter by category'
                            onChange={value => setCategoryFilter(value)}
                            style={{ marginLeft: '10px', marginRight: '10px' }}
                        />
                        <Select
                            data={subcategoryOptions}
                            size='sm'
                            value={subcategoryFilter || ''}
                            placeholder='Filter by subcategory'
                            onChange={value => setSubcategoryFilter(value)}
                            className="filter-select"
                        />
                    </>
                )}
            </div>

            <div style={{ display: 'flex', alignItems: 'center', margin: '10px 0px' }}>
                <Input
                    type="text"
                    placeholder="Search"
                    value={searchTerm}
                    onChange={handleSearchChange}
                    style={{ marginLeft: '10px', marginRight: '10px' }}
                />
            </div>

            <div className="table-container">
                <ScrollArea style={{ height: '75vh', width: '90vw' }}>
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
                        <Table.Tbody style={{ marginLeft: '20px' }}>{rows}</Table.Tbody>
                    </Table>
                </ScrollArea>
            </div>

            <div style={{ display: 'flex', justifyContent: 'center' }}>
                <Pagination
                    total={pageCount}
                    value={currentPage}
                    onChange={handlePageChange}
                    siblings={1}
                />
            </div>
        </div>
    );
}
import React, { useState, useEffect } from 'react';
import { TextInput, Button, Select } from '@mantine/core';

const subcategories = {
    'General Items': ['General Items', 'Printed Items', 'Stationary', 'Toners, Cartridges & Drums'],
    'Medical Items': ['Laboratory Items', 'Laboratory Instruments', 'Laboratory Test Kits', 'Medical Consumable', 'Medical Instruments', 'Oncology Items', 'Pharmaceuticals', 'Radiology Items'],
    'Narcotic': ['Controlled Drugs'],
};

const AddItemPage = () => {
    const [itemCode, setItemCode] = useState(0);
    const [itemDescription, setItemDescription] = useState('');
    const [category, setCategory] = useState('');
    const [subcategory, setSubcategory] = useState('');
    const [unit, setUnit] = useState('');
    const [brand, setBrand] = useState('');
    const [inwards, setInwards] = useState(0);
    const [outwards, setOutwards] = useState(0);
    const [reorder, setReorder] = useState(0);

    useEffect(() => {
        const fetchMaxItemCode = async () => {
            try {
                const response = await fetch('http://localhost:5000/api/maxItemCode');
                const data = await response.json();
                setItemCode((data.maxItemCode || 0) + 1);
            } catch (error) {
                console.error('Error fetching maxItemCode:', error);
            }
        };

        fetchMaxItemCode();
    }, []);

    const handleAddItem = async () => {
        try {
            const response = await fetch('http://localhost:5000/api/addItem', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    item_code: itemCode,
                    item_description: itemDescription,
                    category: category,
                    subcategory: subcategory,
                    unit: unit,
                    brand: brand,
                    inwards: inwards,
                    outwards: outwards,
                    reorder: reorder,
                }),
            });

            if (!response.ok) {
                throw new Error(`Failed to add item: ${response.statusText}`);
            }

            console.log('Item added successfully!');
        } catch (error) {
            console.error('Error adding item:', error);
        }
    };

    const handleCategoryChange = (value) => {
        setCategory(value);
    };

    const handleSubcategoryChange = (value) => {
        setSubcategory(value);
    };

    return (
        <div>
            <TextInput label="Item Code" value={itemCode} onChange={(event) => setItemCode(Number(event.currentTarget.value))} />
            <TextInput label="Item Description" value={itemDescription} onChange={(event) => setItemDescription(event.currentTarget.value)} />
            <Select label="Category" data={Object.keys(subcategories)} value={category} onChange={handleCategoryChange} />
            <Select label="Subcategory" data={subcategories[category]} value={subcategory} onChange={handleSubcategoryChange} />
            <TextInput label="Unit" value={unit} onChange={(event) => setUnit(event.currentTarget.value)} />
            <TextInput label="Brand" value={brand} onChange={(event) => setBrand(event.currentTarget.value)} />
            <TextInput type="number" label="Inwards" value={inwards} onChange={(event) => setInwards(Number(event.currentTarget.value))} />
            <TextInput type="number" label="Outwards" value={outwards} onChange={(event) => setOutwards(Number(event.currentTarget.value))} />
            <TextInput type="number" label="Reorder" value={reorder} onChange={(event) => setReorder(Number(event.currentTarget.value))} />
            <Button onClick={handleAddItem}>Add Item</Button>
        </div>
    );
};

export default AddItemPage;

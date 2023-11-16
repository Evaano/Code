import React from 'react';
import sqlite3 from 'sqlite3';
import { open } from 'sqlite';
import { TextInput, Button, Select } from '@mantine/core';

const subcategories = {
    'General Items': ['General Items', 'Printed Items', 'Stationary', 'Toners, Cartridges & Drums'],
    'Medical Items': ['Laboratory Items', 'Laboratory Instruments', 'Laboratory Test Kits', 'Medical Consumable', 'Medical Instruments', 'Oncology Items', 'Pharmaceuticals', 'Radiology Items'],
    'Narcotic': ['Controlled Drugs'],
};

interface MaxItemCodeRow {
    maxItemCode?: number;
}

export default function AddItemsPage() {
    const [itemCode, setItemCode] = React.useState(0);
    React.useEffect(() => {
        getMaxItemCode().then((maxCode) => {
            setItemCode(maxCode + 1);
        });
    }, []);

    const [itemDescription, setItemDescription] = React.useState('');
    const [category, setCategory] = React.useState('');
    const [subcategory, setSubcategory] = React.useState('');
    const [unit, setUnit] = React.useState('');
    const [brand, setBrand] = React.useState('');
    const [inwards, setInwards] = React.useState('');
    const [outwards, setOutwards] = React.useState('');
    const [currentStock, setCurrentStock] = React.useState('');
    const [reorder, setReorder] = React.useState('');

    function getMaxItemCode(): Promise<number> {
        return new Promise((resolve, reject) => {
            const db = new sqlite3.Database('inventory.db', (err) => {
                if (err) {
                    return reject(err);
                }

                db.get('SELECT MAX(item_code) AS maxItemCode FROM inventory', (err, row: MaxItemCodeRow) => {
                    if (err) {
                        reject(err);
                    } else {
                        resolve(row && row.maxItemCode ? row.maxItemCode : 0);
                    }

                    db.close();
                });
            });
        });
    }

    async function addItemToDatabase(
        itemCode: string,
        itemDescription: string,
        category: string,
        subcategory: string,
        unit: string,
        brand: string,
        inwards: number,
        outwards: number,
        reorder: number
    ) {
        const currentStock = inwards - outwards;

        try {
            const db = await open({
                filename: 'inventory.db',
                driver: sqlite3.Database,
            });

            const existingItemCode = await db.get('SELECT item_code FROM inventory WHERE item_code = ?', itemCode);
            const existingItemDescription = await db.get('SELECT item_description FROM inventory WHERE item_description = ?', itemDescription);

            if (existingItemCode) {
                throw new Error(`Item with Item Code ${itemCode} already exists.`);
            }

            if (existingItemDescription) {
                throw new Error(`Item with Item Description '${itemDescription}' already exists.`);
            }

            await db.run(
                `INSERT INTO inventory
            (item_code, item_description, category, subcategory, unit, brand, inwards, outwards, current_stock, reorder)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
                itemCode,
                itemDescription,
                category,
                subcategory,
                unit,
                brand,
                inwards,
                outwards,
                currentStock,
                reorder
            );

            console.log(`Added item '${itemDescription}' to the inventory.`);
        } catch (err) {
            console.error(err);
        }
    }

    function clearInputFields() {
        getMaxItemCode().then((maxCode) => {
            setItemCode(maxCode + 1);
        });
        setItemDescription('');
        setCategory('');
        setSubcategory('');
        setUnit('');
        setBrand('');
        setInwards('');
        setOutwards('');
        setCurrentStock('');
        setReorder('');
    }

    return (
        <div style={{ padding: '20px' }}>
            //mock form to test adding item to database
            <TextInput label="Item Code" value={itemCode} onChange={(event: React.ChangeEvent<HTMLInputElement>) => setItemCode(parseInt(event.target.value))} />
            <TextInput label="Item Description" value={itemDescription} onChange={(event: React.ChangeEvent<HTMLInputElement>) => setItemDescription(event.target.value)} />
            <Select label="Category" value={category} onChange={(value: string | null) => setCategory(value || '')}>
                <option value="">All</option>
                <option value="General Items">General Items</option>
                <option value="Medical Items">Medical Items</option>
                <option value="Narcotic">Narcotic</option>
            </Select>
            <Select label="Subcategory" value={subcategory} onChange={(value: string | null) => setSubcategory(value || '')}>
                <option value="">All</option>
                {category && subcategories[category].map((subcategory) => <option value={subcategory}>{subcategory}</option>)}
            </Select>
            <TextInput label="Unit" value={unit} onChange={(event: React.ChangeEvent<HTMLInputElement>) => setUnit(event.target.value)} />
            <TextInput label="Brand" value={brand} onChange={(event: React.ChangeEvent<HTMLInputElement>) => setBrand(event.target.value)} />
            <TextInput label="Inwards" value={inwards} onChange={(event: React.ChangeEvent<HTMLInputElement>) => setInwards(event.target.value)} />
            <TextInput label="Outwards" value={outwards} onChange={(event: React.ChangeEvent<HTMLInputElement>) => setOutwards(event.target.value)} />
            <TextInput label="Reorder" value={reorder} onChange={(event: React.ChangeEvent<HTMLInputElement>) => setReorder(event.target.value)} />
            <Button
                variant="outline"
                color="blue"
                onClick={() => {
                    addItemToDatabase(itemCode.toString(), itemDescription, category, subcategory, unit, brand, parseInt(inwards), parseInt(outwards), parseInt(reorder));
                    clearInputFields();
                }}>
                Add Item
            </Button>
        </div>
    );
}

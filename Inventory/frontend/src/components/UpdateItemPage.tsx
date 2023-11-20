import React, { useState, useEffect } from "react";
import { TextInput, Button, Select, Notification } from "@mantine/core";
import classes from "./ContainedInput.module.css";

const subcategories = {
    "General Items": [
        "General Items",
        "Printed Items",
        "Stationary",
        "Toners, Cartridges & Drums",
    ],
    "Medical Items": [
        "Laboratory Items",
        "Laboratory Instruments",
        "Laboratory Test Kits",
        "Medical Consumable",
        "Medical Instruments",
        "Oncology Items",
        "Pharmaceuticals",
        "Radiology Items",
    ],
    Narcotic: ["Controlled Drugs"],
};

const UpdateItemPage = () => {
    const [selectedItem, setSelectedItem] = useState(null);
    const [itemCode, setItemCode] = useState(0);
    const [itemDescription, setItemDescription] = useState("");
    const [category, setCategory] = useState("");
    const [subcategory, setSubcategory] = useState("");
    const [unit, setUnit] = useState("");
    const [brand, setBrand] = useState("");
    const [inwards, setInwards] = useState(0);
    const [outwards, setOutwards] = useState(0);
    const [reorder, setReorder] = useState(0);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const [suggestions, setSuggestions] = useState([]);
    const [debouncedInput, setDebouncedInput] = useState("");

    useEffect(() => {
        // Debounce the keypress events
        const timerId = setTimeout(() => {
            setDebouncedInput(itemDescription);
        }, 500);

        return () => {
            clearTimeout(timerId);
        };
    }, [itemDescription]);

    useEffect(() => {
        // Fetch suggestions based on the debounced input
        if (debouncedInput.trim() !== "") {
            fetchSuggestions(debouncedInput);
        } else {
            // Clear suggestions when the input is empty
            setSuggestions([]);
        }
    }, [debouncedInput]);

    const fetchSuggestions = async (input) => {
        try {
            const response = await fetch(
                `http://localhost:5000/get-item-descriptions?input=${input}`
            );
            const data = await response.json();
            setSuggestions(data);
        } catch (error) {
            console.error("Error fetching suggestions:", error);
        }
    };

    const handleCategoryChange = (value) => {
        setCategory(value);
    };

    const handleSubcategoryChange = (value) => {
        setSubcategory(value);
    };

    const updateItem = async () => {
        try {
            const response = await fetch(`http://localhost:5000/api/update-item`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    item_code: itemCode,
                    item_description: itemDescription,
                    category,
                    subcategory,
                    unit,
                    brand,
                    inwards,
                    outwards,
                    reorder,
                }),
            });

            const data = await response.json();
            if (response.ok) {
                setSuccess(data.message);
            } else {
                setError(data.error);
            }
        } catch (error) {
            console.error("Error updating item:", error);
            setError("Error updating item. Please try again.");
        }
    };

    return (
        <div style={{ width: "43vw", margin: "50px auto", alignItems: "center" }}>
            <TextInput
                label="Item Code"
                value={itemCode}
                onChange={(event) => setItemCode(Number(event.currentTarget.value))}
                error={!itemCode && "Item Code is required"}
                classNames={classes}
            />
            <TextInput
                label="Item Description"
                value={itemDescription}
                onChange={(event) => setItemDescription(event.currentTarget.value)}
                error={!itemDescription && "Item Description is required"}
                classNames={classes}
            />
            {suggestions.length > 0 && (
                <div style={{ maxHeight: '100vh', overflowY: 'auto', width: '100%', overflowX: 'hidden' }}>
                    <strong>Suggestions:</strong>
                    <ul>
                        {suggestions.map((suggestion) => (
                            <li key={suggestion}>{suggestion}</li>
                        ))}
                    </ul>
                </div>
            )}

            <Select
                mt="md"
                comboboxProps={{ withinPortal: true }}
                label="Category"
                placeholder="Pick one"
                data={Object.keys(subcategories)}
                value={category}
                onChange={handleCategoryChange}
                classNames={classes}
                error={!category && "Category is required"}
                style={{ display: "inline-block" }}
            />
            <Select
                mt="md"
                label="Subcategory"
                data={subcategories[category]}
                value={subcategory}
                placeholder="Pick one"
                onChange={handleSubcategoryChange}
                classNames={classes}
                error={!subcategory && "Subcategory is required"}
                style={{ display: "inline-block" }}
            />
            <TextInput
                label="Unit"
                value={unit}
                onChange={(event) => setUnit(event.currentTarget.value)}
                error={!unit && "Unit is required"}
                classNames={classes}
                style={{ display: "inline-block" }}
            />
            <TextInput
                label="Brand"
                placeholder="Optional"
                value={brand}
                onChange={(event) => setBrand(event.currentTarget.value)}
                classNames={classes}
            />
            <TextInput
                type="number"
                label="Inwards"
                value={inwards}
                onChange={(event) => setInwards(Number(event.currentTarget.value))}
                classNames={classes}
            />
            <TextInput
                type="number"
                label="Outwards"
                value={outwards}
                onChange={(event) => setOutwards(Number(event.currentTarget.value))}
                classNames={classes}
            />
            <TextInput
                type="number"
                label="Reorder"
                value={reorder}
                onChange={(event) => setReorder(Number(event.currentTarget.value))}
                classNames={classes}
            />
            {success && <Notification>{success}</Notification>}
            {error && <Notification>{error}</Notification>}
            <Button onClick={updateItem} style={{ margin: "10px" }}>
                Update
            </Button>
        </div>
    );
};

export default UpdateItemPage;

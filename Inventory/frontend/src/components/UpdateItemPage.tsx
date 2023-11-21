import React, { useState, useEffect } from "react";
import { TextInput, Button, Select, Notification, Title, Text } from "@mantine/core";
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

const units = [
    "Ampule", "Bag", "Bottle", "Bottles",
    "Box", "Can", "Caps", "Case", "Kit",
    "Meter", "Numbers", "Packet", "Pad", "Pair",
    "Pieces", "Ream", "Roll", "Set", "Sheet",
    "Sheets", "Tab", "Tablet", "Tin", "Tube", "Unit",
    "Vial", "Vials"];

const UpdateItemPage = () => {
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
        const timerId = setTimeout(() => {
            setDebouncedInput(itemDescription);
        }, 500);

        return () => {
            clearTimeout(timerId);
        };
    }, [itemDescription]);

    useEffect(() => {
        if (debouncedInput.trim() !== "") {
            fetchSuggestions(debouncedInput);
        } else {
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

    const handleSuggestionClick = async (selectedSuggestion) => {
        setItemDescription(selectedSuggestion);
        setSuggestions([]);

        try {
            const response = await fetch("http://localhost:5000/search-item", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    selected_option: selectedSuggestion,
                }),
            });

            const data = await response.json();
            if (response.ok) {
                setItemCode(data.item_code || 0);
                setCategory(data.category || "");
                setSubcategory(data.subcategory || "");
                setUnit(data.unit || "");
                setBrand(data.brand || "");
                setInwards(data.inwards || 0);
                setOutwards(data.outwards || 0);
                setReorder(data.reorder || 0);
            } else {
                setError("Error retrieving item details");
            }
        } catch (error) {
            console.error("Error retrieving item details:", error);
            setError("Error retrieving item details. Please try again.");
        }
    };

    const handleCategoryChange = (value) => {
        setCategory(value);
    };

    const handleSubcategoryChange = (value) => {
        setSubcategory(value);
    };

    const updateItem = async () => {
        if (!itemCode || !itemDescription || !category || !subcategory || !unit) {
            setError("All fields are required");
            return;
        }

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

    const deleteItem = async () => {
        if (!itemCode) {
            setError("Item Code is required");
            return;
        }

        try {
            const response = await fetch(`http://localhost:5000/api/delete-item`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    item_code: itemCode,
                }),
            });

            const data = await response.json();
            if (response.ok) {
                setSuccess(data.message);
                setItemCode(0);
                setItemDescription("");
            } else {
                setError(data.error);
            }
        } catch (error) {
            console.error("Error deleting item:", error);
            setError("Error deleting item. Please try again.");
        }
    };

    return (
        <div style={{ width: "90vw", display: "flex", justifyContent: "center", alignItems: "center", marginTop: '20px', marginLeft: '20px' }}>
            <div style={{ width: "44vw" }}>
                <Title order={1}><Text span c="green" inherit>Update</Text>  an existing Item</Title>
                <div style={{ width: "43vw", margin: "50px auto", alignItems: "center" }}>
                    <TextInput
                        label="Item Code"
                        value={itemCode}
                        onChange={(event) => setItemCode(Number(event.currentTarget.value))}
                        error={!itemCode && "Item Code is required"}
                        classNames={classes}
                        style={{ width: "100px", marginTop: '20px' }}
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
                                    <li key={suggestion} onClick={() => handleSuggestionClick(suggestion)}>
                                        {suggestion}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}
                    <Select
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
                        label="Subcategory"
                        data={subcategories[category]}
                        value={subcategory}
                        placeholder="Pick one"
                        onChange={handleSubcategoryChange}
                        classNames={classes}
                        error={!subcategory && "Subcategory is required"}
                        style={{ display: "inline-block" }}
                    />
                    <Select
                        label="Unit"
                        data={units}
                        value={unit}
                        placeholder="Pick one"
                        onChange={(value) => setUnit(value)}
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
                    <Button onClick={deleteItem} style={{ margin: "10px" }}>
                        Delete
                    </Button>
                </div>
            </div>
        </div>
    );
};

export default UpdateItemPage;

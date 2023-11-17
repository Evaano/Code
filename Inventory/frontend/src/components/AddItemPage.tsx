import React, { useState, useEffect } from "react";
import { TextInput, Button, Select, Text, Notification } from "@mantine/core";
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

const AddItemPage = () => {
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

  useEffect(() => {
    const fetchMaxItemCode = async () => {
      try {
        const response = await fetch("http://localhost:5000/api/maxItemCode");
        const data = await response.json();
        setItemCode((data.maxItemCode || 0) + 1);
      } catch (error) {
        console.error("Error fetching maxItemCode:", error);
      }
    };

    fetchMaxItemCode();
  }, []);

  const handleAddItem = async () => {
    if (!itemCode || !itemDescription || !category || !subcategory || !unit) {
      setError("All fields are required");
      return;
    }

    setError("");
    try {
      const response = await fetch("http://localhost:5000/api/addItem", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
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

      setSuccess("Item added successfully!");
      console.log("Item added successfully!");
    } catch (error) {
      console.error("Error adding item:", error);
    }
  };

  const handleCategoryChange = (value) => {
    setCategory(value);
  };

  const handleSubcategoryChange = (value) => {
    setSubcategory(value);
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
      <Button onClick={handleAddItem} style={{ margin: '10px' }}>Add Item</Button>
    </div>
  );
};

export default AddItemPage;

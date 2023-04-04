import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import React, { useState } from 'react';
import tw from 'twrnc';
import { SafeAreaView } from 'react-native-safe-area-context';
import { FlatList } from 'react-native-gesture-handler';
import { Image } from '@rneui/themed/dist/Image';

const data = [
  {
    id: 'Uber-X-123',
    title: 'Car',
    price: 'MVR 85',
    image: 'https://links.papareact.com/3pn'
  },
  {
    id: 'Uber-X-456',
    title: 'Van',
    price: 'MVR 85',
    image: 'https://links.papareact.com/5w8'
  },
  {
    id: 'Uber-LUX-789',
    title: 'Bike',
    price: 'MVR 60',
    image: 'https://i.imgur.com/XDtr2Nc.png'
  },
]

const RideOptionsCard = () => {
  const [selected, setSelected] = useState(null);

  return (
    <SafeAreaView>
      <View>
        <Text style={tw`text-center py-5 text-xl`}>Select a Ride</Text>
      </View>

      <FlatList data={data}
        keyExtractor={(item) => item.id}
        renderItem={({ item: { id, title, price, image }, item }) => (
          <TouchableOpacity onPress={() => setSelected(item)} 
            style={tw`px-14 flex-row items-center justify-between ${id == selected?.id && 'bg-gray-300'}`}>
            <Image
              style={{
                width: 100,
                height: 100,
                resizeMode: 'contain',
              }}
              source={{ uri: image }}
            />

            <View>
              <Text style={tw`font-bold text-xl`}>{title}</Text>
              <Text style={tw`font-semibold`}>{price}</Text>
            </View>
          </TouchableOpacity>
        )}
      />
      <TouchableOpacity disabled={!selected} style={tw`bg-black py-2 m-1 mx-26 rounded-full ${!selected && 'bg-gray-300'}`}>
        <Text style={tw`text-center text-white text-xl`}>Choose {selected?.title}</Text>
      </TouchableOpacity>
    </SafeAreaView>
  );
};

export default RideOptionsCard;

const styles = StyleSheet.create({});
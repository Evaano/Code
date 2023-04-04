import { FlatList, Text, TouchableOpacity, View, Image } from 'react-native';
import React from 'react';
import tw from 'twrnc';
import { Icon } from '@rneui/themed';
import { useNavigation } from '@react-navigation/native';

const data = [
  {
    id: "123",
    title: "Get a Ride",
    image: "https://www.uber-assets.com/image/upload/f_auto,q_auto:eco,c_fill,w_698,h_465/v1568070443/assets/82/6bf372-6016-492d-b20d-d81878a14752/original/Black.png",
    screen: "MapScreen",
  },
];

const NavOptions = () => {
  const navigation = useNavigation();

  return (
    <FlatList
      data={data}
      horizontal
      keyExtractor={(item) => item.id}
      renderItem={({ item }) => (
        <TouchableOpacity onPress={() => navigation.navigate(item.screen)} 
        style={tw`p-2 items-center`}>
          <View>
            <Image
            style={{ width: 380, height: 500, resizeMode: 'contain', alignItems: 'center' }}

              source={{ uri: item.image }}
            />
            <View style={tw`flex items-center justify-center`}>
              <Text style={tw`mt-2 text-lg font-semibold pl-5.5 text-center pb-5`}>{item.title}</Text>
              <Icon style={tw`p-1 bg-gray-600 rounded-full w-9`}
                name='arrowright' type='antdesign' color='white' />
            </View>
          </View>
        </TouchableOpacity>
      )}
    />
  );
};

export default NavOptions;

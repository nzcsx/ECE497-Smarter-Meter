import React from 'react';
import {
    PanResponder,
    Dimensions,
    Text,
    TouchableOpacity,
    View,
    TextInput,
  StyleSheet,
  ScrollView,
  Button,
  Image,
  
} from 'react-native';
import { PieChart } from 'react-native-svg-charts'

 class SpatialScreen extends React.PureComponent {

    constructor(props) {
        super(props);
        this.state = {
        selectedSlice: {
            label: '',
            value: 0
        },
        labelWidth: 0,
        keys: ['google', 'facebook', 'linkedin', 'youtube', 'Twitter'],
        values:[15, 25, 35, 45, 55],
        colors:['#600080', '#9900cc', '#c61aff', '#d966ff', '#ecb3ff'],
        }
    }

    onChangeText = (key, val) => {
        this.setState({ [key]: val })
    }

    GetReport = async () => {
        //const { username, password, family, reset_Q, reset_A, confirm_password } = this.state

        info = "date1="+this.state.start_date+"&date2="+this.state.end_date;
        console.log(info);

        fetch("http://127.0.0.1:5000/spatial", {method: "POST",
            body: info, 
            header: {
                'Content-Type': 'application/json'
              } // <-- Post parameters        
        })
        .then((response) => response.json())
        .then((responseJson) => {
           console.log(responseJson);
        //    this.setState({
        //       data: responseJson
        //    })
            verification = responseJson.report;
            this.setState({values: responseJson.values, keys: responseJson.appliance});

            

        })
        .catch((error) => {
           console.error(error);
        });
    }



    render() {
        const { labelWidth, selectedSlice } = this.state;
        const { label, value } = selectedSlice;
        //const keys = ['google', 'facebook', 'linkedin', 'youtube', 'Twitter'];
        // const values = [15, 25, 35, 45, 55];
        // const colors = ['#600080', '#9900cc', '#c61aff', '#d966ff', '#ecb3ff']
        const data = this.state.keys.map((key, index) => {
            return {
            key,
            value: this.state.values[index],
            svg: { fill: this.state.colors[index] },
            arc: { outerRadius: (70 + this.state.values[index]/4) + '%', padAngle: label === key ? 0.1 : 0 },
            onPress: () => this.setState({ selectedSlice: { label: key, value: this.state.values[index] } })
            }
        })
        const deviceWidth = Dimensions.get('window').width

        return (
        <View style={{ justifyContent: 'center', flex: 1 }}>
            
            <PieChart
            style={{ height: 400 }}
            outerRadius={'80%'}
            innerRadius={'45%'}
            data={data}
            />
            <Text
            onLayout={({ nativeEvent: { layout: { width } } }) => {
                this.setState({ labelWidth: width });
            }}
            style={{
                position: 'absolute',
    
                top:'36.5%',
                left: deviceWidth / 2 - labelWidth / 2,
                textAlign: 'center'
            }}>
            {`${label} \n ${value}`}
            </Text>

            <View style={{ flexDirection:"row" }}>
                    <Text style={[styles.text2]}>
                            From: 
                    </Text>
                    <TextInput
                        style={styles.input}
                        placeholder='Start Date (YYYY-MM-DD)'
                        autoCapitalize="none"
                        placeholderTextColor='white'
                        onChangeText={val => this.onChangeText('start_date', val)}
                    />
                </View>

                <View style={{ flexDirection:"row" }}>
                    <Text style={[styles.text2]}>
                            To  :   
                    </Text>
                    <TextInput
                        style={styles.input}
                        placeholder='End Date (YYYY-MM-DD)'
                        autoCapitalize="none"
                        placeholderTextColor='white'
                        onChangeText={val => this.onChangeText('end_date', val)}
                    />
                </View>

                <View style={{ flexDirection:"row", position: 'relative', height: 50, alignItems: 'center', justifyContent: 'center', }}>
                    <Button
                    title='Get Report'
                    onPress={this.GetReport}
                    />

                    <Button
                    title='Home'
                    onPress={() => {this.props.navigation.navigate('NestedReport') }}
                    />
                </View>

        </View>
        
        )
    }
}

const styles = StyleSheet.create({
    logo: {
        resizeMode: "cover",
        width: 130,
        height: 130,
        margin: 20,
    },
    input: {
        width: 240,
        height: 35,
        backgroundColor: '#83cfe3',
        margin: 10,
        padding: 8,
        color: 'white',
        borderRadius: 14,
        fontSize: 18,
        fontWeight: '500',
    },
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center'
    },
    text: {
        fontSize: 30,
        margin: 10,
        
    },
    text2: {
        fontSize: 20,
        margin: 10,
        
    },
    text3: {
        fontSize: 11,
        margin: 10,
        
    },
})

export default SpatialScreen;


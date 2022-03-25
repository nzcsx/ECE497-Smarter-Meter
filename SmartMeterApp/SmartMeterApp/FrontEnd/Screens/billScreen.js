import React from 'react'
import {     PanResponder,
    Dimensions,
    TouchableOpacity,
    View,
    TextInput,
  StyleSheet,
  ScrollView,
  Button,
  Image,} from 'react-native'
import { BarChart, Grid } from 'react-native-svg-charts'
import { Text } from 'react-native-svg'

class billScreen extends React.PureComponent {

    constructor(props) {
        super(props);
        this.state = {

        data:[15, 25, 35, 45, 55],
        dates: [1, 2, 3, 4, 5],
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

        fetch("http://127.0.0.1:5000/bill", {method: "POST",
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
            this.setState({data: responseJson.values, dates: responseJson.dates});

            

        })
        .catch((error) => {
           console.error(error);
        });
    }

    render() {


        const CUT_OFF = 10
        const Labels = ({  x, y, bandwidth, data }) => (
            data.map((value, index) => (
                <Text
                    key={ index }
                    x={ value > CUT_OFF ? x(0) + 10 : x(value) + 10 }
                    y={ y(index) + (bandwidth / 2) }
                    fontSize={ 14 }
                    fill={ value > CUT_OFF ? 'white' : 'black' }
                    alignmentBaseline={ 'middle' }
                >
                    {value}
                </Text>
            ))
        )

        return (
            // need to add y-axis
            <View style={{  height: 600, paddingVertical: 30 }}>
                <BarChart
                    style={{ flex: 1, marginLeft: 8 }}
                    data={this.state.data}
                    horizontal={true}
                    svg={{ fill: 'rgba(134, 65, 244, 0.8)' }}
                    contentInset={{ top: 10, bottom: 10 }}
                    spacing={0.2}
                    gridMin={0}
                >
                    <Grid direction={Grid.Direction.VERTICAL}/>
                    <Labels/>
                </BarChart>

                <View style={{ flexDirection:"row", position: 'relative', height: 50, alignItems: 'center', justifyContent: 'center', }}>
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

                <View style={{ flexDirection:"row", position: 'relative', height: 50, alignItems: 'center', justifyContent: 'center', }}>
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

export default billScreen;
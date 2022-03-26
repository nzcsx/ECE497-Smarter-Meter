import React from 'react'
import {
    PanResponder,
    Dimensions,
    TouchableOpacity,
    View,
    TextInput,
  StyleSheet,
  ScrollView,
  Button,
  Image,
  Text
  
} from 'react-native';
import * as shape from 'd3-shape'
import { Grid, LineChart, XAxis, YAxis } from 'react-native-svg-charts'

class TemporalScreen extends React.PureComponent {
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

        fetch("http://127.0.0.1:5000/temporal", {method: "POST",
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
            this.setState({data: responseJson.readings, dates: responseJson.dates});

            

        })
        .catch((error) => {
           console.error(error);
        });
    }

    render() {


        /**
         * Both below functions should preferably be their own React Components
         */
         const axesSvg = { fontSize: 10, fill: 'grey' };
         const verticalContentInset = { top: 10, bottom: 10 }
         const xAxisHeight = 30

        const HorizontalLine = (({ y }) => (
            <Line
                key={ 'zero-axis' }
                x1={ '0%' }
                x2={ '100%' }
                y1={ y(50) }
                y2={ y(50) }
                stroke={ 'grey' }
                strokeDasharray={ [ 4, 8 ] }
                strokeWidth={ 2 }
            />
        ))

        const Tooltip = ({ x, y }) => (
            <G
                x={ x(5) - (75 / 2) }
                key={ 'tooltip' }
                onPress={ () => console.log('tooltip clicked') }
            >
                <G y={ 50 }>
                    <Rect
                        height={ 40 }
                        width={ 75 }
                        stroke={ 'grey' }
                        fill={ 'white' }
                        ry={ 10 }
                        rx={ 10 }
                    />
                    <Text
                        x={ 75 / 2 }
                        dy={ 20 }
                        alignmentBaseline={ 'middle' }
                        textAnchor={ 'middle' }
                        stroke={ 'rgb(134, 65, 244)' }
                    >
                        { `${this.state.data[5]}ºC` }
                    </Text>
                </G>
                <G x={ 75 / 2 }>
                    <Line
                        y1={ 50 + 40 }
                        y2={ y(this.state.data[ 5 ]) }
                        stroke={ 'grey' }
                        strokeWidth={ 2 }
                    />
                    <Circle
                        cy={ y(this.state.data[ 5 ]) }
                        r={ 6 }
                        stroke={ 'rgb(134, 65, 244)' }
                        strokeWidth={ 2 }
                        fill={ 'white' }
                    />
                </G>
            </G>
        )

        return (

            <View style={{ justifyContent: 'center', flex: 1 }}>
            
            <View style={{ height: 200, padding: 20, flexDirection: 'row' }}>
            <YAxis
                data={this.state.data}
                style={{ marginBottom: xAxisHeight }}
                contentInset={verticalContentInset}
                svg={axesSvg}
            />
            <View style={{ flex: 1, marginLeft: 10 }}>
                <LineChart
                    style={{ flex: 1 }}
                    data={this.state.data}
                    contentInset={verticalContentInset}
                    svg={{ stroke: 'rgb(134, 65, 244)' }}
                >
                    <Grid/>
                </LineChart>
                <XAxis
                    style={{ marginHorizontal: -10, height: xAxisHeight }}
                    data={this.state.data}
                    formatLabel={(value, index) => index}
                    contentInset={{ left: 10, right: 10 }}
                    svg={axesSvg}
                />
            </View>
            

            </View>
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

export default TemporalScreen
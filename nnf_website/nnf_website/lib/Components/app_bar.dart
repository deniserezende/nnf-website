import 'package:flutter/material.dart';
import 'simple_button.dart';
import 'menu_item.dart';
import 'constants.dart';

class CustomAppBar extends StatelessWidget {
  const CustomAppBar({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    Size size = MediaQuery.of(context).size;
    return Container(
      margin: EdgeInsets.all(size.height * 0.05),
      padding: EdgeInsets.all(size.height * 0.025),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(46),
        boxShadow: [
          BoxShadow(
            offset: const Offset(0,-2),
            blurRadius: 30,
            color: Colors.black.withOpacity(0.16),
            ),
          ],
        ),
      child: Row(
        
        children: <Widget> [
          //Image.asset("assets/images/icon.jpg", 
          //  height: 25,
          //  alignment: Alignment.topCenter,
          //  ),
          const SizedBox(width: 5.0,),
          const Text(
            "nNF", 
            style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: kDarkBlueColorT1),
            ),
          const Spacer(),
          MenuItem(
            title: "Home", 
            press: (){

            },
          ),
          MenuItem(
            title: "About", 
            press: (){

            },
          ),
          MenuItem(
            title: "Pricing", 
            press: (){

            },
          ),
          MenuItem(
            title: "Contact", 
            press: (){

            },
          ),
          MenuItem(
            title: "Login", 
            press: (){

            },
          ),
          SimpleButton(
            text: "Get Started", 
            press: (){}
          ),
          
        ],
      ),
    );
  }
}


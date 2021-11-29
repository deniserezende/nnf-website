import 'package:flutter/material.dart';

import 'constants.dart';

class SimpleButton extends StatelessWidget {
  final String text;
  final Function press;
  const SimpleButton(
    { Key? key, 
    required this.text, 
    required this.press, 
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      child: Text(
        text.toUpperCase()
      ),
      onPressed: (){
        press();
      }, 
      style: ElevatedButton.styleFrom(
        primary: kPrimaryColor,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(20),
        ),
        minimumSize: const Size(40, 50),
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
      ),
      
    );
  }
}
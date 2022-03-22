using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;

public class MouseHoverGrow : MonoBehaviour, IPointerEnterHandler, IPointerExitHandler
{
    public Animator anim;
    public string animName;

    public void OnPointerEnter(PointerEventData eventData)
    {
        anim.SetBool("MouseOver"+animName, true);
        Invoke("EnterNext", 0.01f);
    }

    void EnterNext()
    {
        anim.SetBool("MouseIsOver"+animName, true);
    }

    public void OnPointerExit(PointerEventData eventData)
    {
        anim.SetBool("MouseOver"+animName, false);
        anim.SetBool("MouseIsOver"+animName, false);
    }
}

#ifndef FIX64QUATERNION_H
#define FIX64QUATERNION_H

#include "Fix64Vector3.h"


struct Fix64Quaternion
{
	Fix64Scalar m_x;
	Fix64Scalar m_y;
	Fix64Scalar m_z;
	Fix64Scalar m_w;

	Fix64Scalar getX() const
	{
		return m_x;
	}
	Fix64Scalar getY() const
	{
		return m_y;
	}
	Fix64Scalar getZ() const
	{
		return m_z;
	}
	Fix64Scalar getW() const
	{
		return m_w;
	}

	void setValue(const Fix64Scalar&x, const Fix64Scalar&y, const Fix64Scalar&z, const Fix64Scalar&w)
	{
		m_x=x;
		m_y=y;
		m_z=z;
		m_w=w;
	}

	static Fix64Quaternion makeIdentity()
	{
		Fix64Quaternion res;
		res.setValue(Fix64Scalar::zero(),Fix64Scalar::zero(),Fix64Scalar::zero(), Fix64Scalar::one());
		return res;
	}

	static Fix64Quaternion create(const Fix64Scalar&x, const Fix64Scalar&y, const Fix64Scalar&z, const Fix64Scalar&w)
	{
		Fix64Quaternion res;
		res.setValue(x,y,z,w);
		return res;
	}

	B3_FORCE_INLINE Fix64Quaternion operator-() const
	{
		const Fix64Quaternion& q2 = *this;
		return Fix64Quaternion::create( - q2.getX(), - q2.getY(),  - q2.getZ(),  - q2.getW());
	}

	Fix64Quaternion inverse() const
	{
		return Fix64Quaternion::create(-m_x, -m_y, -m_z, m_w);
	}

	Fix64Scalar dot(const Fix64Quaternion& q) const
	{
		return  m_x * q.getX() + 
                m_y * q.getY() + 
                m_z * q.getZ() + 
                m_w * q.getW();
	}

	Fix64Scalar length2() const
	{
		return dot(*this);
	}


	Fix64Quaternion& operator*=(const Fix64Quaternion& q)
	{
		setValue(
            m_w * q.getX() + m_x * q.m_w + m_y * q.getZ() - m_z * q.getY(),
			m_w * q.getY() + m_y * q.m_w + m_z * q.getX() - m_x * q.getZ(),
			m_w * q.getZ() + m_z * q.m_w + m_x * q.getY() - m_y * q.getX(),
			m_w * q.m_w - m_x * q.getX() - m_y * q.getY() - m_z * q.getZ());
		return *this;
	}
	B3_FORCE_INLINE Fix64Quaternion
	operator*(const Fix64Scalar& s) const
	{
		return Fix64Quaternion::create(getX() * s, getY() * s, getZ() * s, getW() * s);
	}

	Fix64Quaternion& operator*=(const Fix64Scalar& s)
	{
		m_x = m_x*s; 
        m_y = m_y*s; 
        m_z = m_z*s; 
        m_w = m_w*s;
		return *this;
	}

	Fix64Quaternion& operator/=(const Fix64Scalar& s) 
	{
		b3Assert(s != Fix64Scalar::zero());
		return *this *= (Fix64Scalar::one() / s);
	}

	B3_FORCE_INLINE	Fix64Quaternion& operator+=(const Fix64Quaternion& q)
	{
		m_x += q.getX(); 
        m_y += q.getY(); 
        m_z += q.getZ(); 
        m_w += q.getW();
		return *this;
	}
	
	B3_FORCE_INLINE Fix64Scalar length() const
	{
		Fix64Scalar res = (*this).dot(*this);
		res = Fix64Scalar::sqrt(res);
		return res;
	}
	

	Fix64Quaternion& normalize() 
	{
		return *this /= length();

	}
	
};




B3_FORCE_INLINE Fix64Quaternion
operator*(const Fix64Vector3& w, const Fix64Quaternion& q)
{
	return Fix64Quaternion::create( 
        w.getX() * q.getW() + w.getY() * q.getZ() - w.getZ() * q.getY(),
		w.getY() * q.getW() + w.getZ() * q.getX() - w.getX() * q.getZ(),
		w.getZ() * q.getW() + w.getX() * q.getY() - w.getY() * q.getX(),
		-w.getX() * q.getX() - w.getY() * q.getY() - w.getZ() * q.getZ()); 

}

B3_FORCE_INLINE Fix64Quaternion
operator*(const Fix64Quaternion& q1, const Fix64Quaternion& q2) 
{
	return Fix64Quaternion::create(
        q1.getW() * q2.getX() + q1.getX() * q2.getW() + q1.getY() * q2.getZ() - q1.getZ() * q2.getY(),
		q1.getW() * q2.getY() + q1.getY() * q2.getW() + q1.getZ() * q2.getX() - q1.getX() * q2.getZ(),
		q1.getW() * q2.getZ() + q1.getZ() * q2.getW() + q1.getX() * q2.getY() - q1.getY() * q2.getX(),
		q1.getW() * q2.getW() - q1.getX() * q2.getX() - q1.getY() * q2.getY() - q1.getZ() * q2.getZ()); 
}


B3_FORCE_INLINE Fix64Quaternion
operator*(const Fix64Quaternion& q, const Fix64Vector3& w)
{
	return Fix64Quaternion::create( 
         q.getW() * w.getX() + q.getY() * w.getZ() - q.getZ() * w.getY(),
		 q.getW() * w.getY() + q.getZ() * w.getX() - q.getX() * w.getZ(),
		 q.getW() * w.getZ() + q.getX() * w.getY() - q.getY() * w.getX(),
		-q.getX() * w.getX() - q.getY() * w.getY() - q.getZ() * w.getZ()); 

}

B3_FORCE_INLINE Fix64Vector3 
Fix64QuatRotate(const Fix64Quaternion& rotation, const Fix64Vector3& v) 
{
	Fix64Quaternion q = rotation * v;

	q *= rotation.inverse();
	
	return Fix64Vector3::create(q.m_x,q.m_y,q.m_z);
}


#endif

